import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Category Training Examples
# --------------------------------------------------
# Synthetic examples used only for classification.
# FAQ answers still come exclusively from the
# knowledge base through the RAG retriever.
# --------------------------------------------------

CATEGORY_EXAMPLES = {
    "billing": [
        "I have a billing problem",
        "My payment was declined",
        "I was charged twice",
        "There is an incorrect charge on my invoice",
        "How do I update my credit card",
        "How do I change my payment method",
        "I need help with my subscription",
        "How do I cancel my plan",
        "I want a refund",
        "Where can I find my invoice"
    ],

    "technical": [
        "The dashboard is not loading",
        "The application is not working",
        "I am getting an error",
        "The page keeps crashing",
        "There is a bug in the system",
        "My API request is failing",
        "I have an integration problem",
        "The website is very slow",
        "The feature is broken",
        "I need technical support"
    ],

    "account_access": [
        "I forgot my password",
        "I cannot log in",
        "My account is locked",
        "How do I reset my password",
        "I cannot access my account",
        "I have a login problem",
        "My verification code is not working",
        "I need help with two factor authentication",
        "I cannot sign in",
        "I lost access to my account"
    ]
}


# --------------------------------------------------
# Text Preprocessing
# --------------------------------------------------

def preprocess_text(text):
    """
    Normalize text before classification.
    """

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


# --------------------------------------------------
# Prepare Training Data
# --------------------------------------------------

training_texts = []
training_labels = []

for category, examples in CATEGORY_EXAMPLES.items():

    for example in examples:

        training_texts.append(
            preprocess_text(example)
        )

        training_labels.append(category)


# --------------------------------------------------
# Initialize TF-IDF Model
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)


training_vectors = vectorizer.fit_transform(
    training_texts
)


# --------------------------------------------------
# Classify Ticket
# --------------------------------------------------

def classify_ticket(message):
    """
    Classify a support message into one of:

    - billing
    - technical
    - account_access

    Returns:
        {
            "category": str,
            "confidence": float,
            "category_scores": dict
        }
    """

    if not message or not message.strip():

        return {
            "category": "unknown",
            "confidence": 0.0,
            "category_scores": {}
        }


    processed_message = preprocess_text(message)

    message_vector = vectorizer.transform(
        [processed_message]
    )


    # Calculate similarity between the incoming
    # message and every training example.
    similarities = cosine_similarity(
        message_vector,
        training_vectors
    )[0]


    # ------------------------------------------------
    # Calculate Best Score for Each Category
    # ------------------------------------------------

    category_scores = {}

    for category in CATEGORY_EXAMPLES:

        category_similarities = [

            similarities[index]

            for index, label in enumerate(training_labels)

            if label == category
        ]


        category_scores[category] = float(
            max(category_similarities)
        )


    # ------------------------------------------------
    # Select Best Category
    # ------------------------------------------------

    best_category = max(
        category_scores,
        key=category_scores.get
    )


    best_score = category_scores[best_category]


    # If there is almost no similarity with any
    # category, treat it as unknown.
    if best_score < 0.10:

        return {
            "category": "unknown",
            "confidence": round(best_score, 4),
            "category_scores": {
                category: round(score, 4)
                for category, score in category_scores.items()
            }
        }


    return {
        "category": best_category,
        "confidence": round(best_score, 4),
        "category_scores": {
            category: round(score, 4)
            for category, score in category_scores.items()
        }
    }


# --------------------------------------------------
# Get Classification Explanation
# --------------------------------------------------

def get_classification_explanation(result):
    """
    Create a human-readable explanation of the
    classification result.
    """

    category = result["category"]
    confidence = result["confidence"]


    if category == "unknown":

        return (
            "The message did not match any of the "
            "supported ticket categories strongly enough."
        )


    return (
        f"The message is most similar to examples in "
        f"the '{category}' category with a classification "
        f"confidence of {confidence:.2f}."
    )


# --------------------------------------------------
# Test the Classifier
# --------------------------------------------------

if __name__ == "__main__":

    test_messages = [
        "I forgot my password and cannot login",
        "Why was my credit card charged twice?",
        "The dashboard keeps crashing",
        "Can you recommend a good movie?"
    ]


    print("\nCloudDesk Ticket Classifier")
    print("=" * 55)


    for message in test_messages:

        result = classify_ticket(message)

        print(f"\nMessage: {message}")

        print(
            f"Category: {result['category']}"
        )

        print(
            f"Confidence: {result['confidence']}"
        )

        print(
            "Scores:",
            result["category_scores"]
        )

        print(
            "Explanation:",
            get_classification_explanation(result)
        )


# --------------------------------------------------
# Escalation / Decision Logic
# --------------------------------------------------


def evaluate_query(classification, retrieval_results):
    """
    Decide whether to answer, ask for clarification, or
    escalate to a human based on classification and
    retrieval confidence.

    Returns a dict containing at least:
        - action: "answer" | "clarify" | "escalate"
        - reason: human-readable explanation
        - retrieval_confidence: float
        - reason_code: optional short code for escalate
    """

    best_score = 0.0

    if retrieval_results:
        best_score = float(retrieval_results[0].get("score", 0.0))


    # Rule: if we have a reasonably confident retrieval and
    # classification isn't unknown, answer directly.
    if best_score >= 0.25 and classification.get("category") != "unknown":
        return {
            "action": "answer",
            "reason": "Knowledge-base retrieval is confident.",
            "retrieval_confidence": round(best_score, 4)
        }


    # If classification is very uncertain, ask a clarifying question.
    if classification.get("confidence", 0.0) < 0.12:
        return {
            "action": "clarify",
            "reason": "I couldn't determine the ticket category with confidence.",
            "retrieval_confidence": round(best_score, 4)
        }


    # If retrieval failed or is below threshold, escalate.
    if best_score < 0.20:
        return {
            "action": "escalate",
            "reason": "No reliable knowledge-base answer found; escalation recommended.",
            "retrieval_confidence": round(best_score, 4),
            "reason_code": "NO_RETRIEVAL"
        }


    # Fallback: ask for clarification when unsure about which FAQ fits.
    return {
        "action": "clarify",
        "reason": "I need a little more information to provide an accurate answer.",
        "retrieval_confidence": round(best_score, 4)
    }


def build_escalation_message(decision):
    """
    Build a human-readable escalation message summarizing
    why the ticket is being escalated.
    """

    reason = decision.get("reason", "Escalating for human review.")
    code = decision.get("reason_code")

    if code:
        return f"Escalation required ({code}): {reason}"

    return f"Escalation required: {reason}"