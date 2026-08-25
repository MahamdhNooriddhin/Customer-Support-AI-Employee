import json
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge_base.json")


# Minimum similarity required for a reliable retrieval
RETRIEVAL_THRESHOLD = 0.20


# --------------------------------------------------
# Load Knowledge Base
# --------------------------------------------------

def load_knowledge_base():
    """
    Load FAQ documents from knowledge_base.json.
    """

    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    return documents


# --------------------------------------------------
# Text Preprocessing
# --------------------------------------------------

def preprocess_text(text):
    """
    Basic text normalization.

    - Converts text to lowercase
    - Removes unnecessary characters
    - Normalizes whitespace
    """

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


# --------------------------------------------------
# Initialize RAG Retriever
# --------------------------------------------------

knowledge_base = load_knowledge_base()


documents = [
    preprocess_text(
        f"{document['title']} {document['content']}"
    )
    for document in knowledge_base
]


vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)


document_vectors = vectorizer.fit_transform(documents)


# --------------------------------------------------
# Retrieve Relevant Documents
# --------------------------------------------------

def retrieve_documents(query, top_k=3):
    """
    Retrieve the most relevant knowledge-base documents.

    Returns:
        A list containing document information and
        similarity scores.
    """

    if not query or not query.strip():
        return []

    processed_query = preprocess_text(query)

    query_vector = vectorizer.transform([processed_query])

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]


    ranked_indices = similarities.argsort()[::-1][:top_k]


    results = []

    for index in ranked_indices:

        score = float(similarities[index])

        document = knowledge_base[index]

        results.append({
            "id": document["id"],
            "category": document["category"],
            "title": document["title"],
            "content": document["content"],
            "score": round(score, 4)
        })


    return results


# --------------------------------------------------
# Get Best Retrieval Result
# --------------------------------------------------

def get_best_document(query):
    """
    Return the single best matching document.

    If the similarity score is below the retrieval
    threshold, return no reliable document.
    """

    results = retrieve_documents(query, top_k=1)

    if not results:
        return None

    best_result = results[0]

    if best_result["score"] < RETRIEVAL_THRESHOLD:
        return None

    return best_result


# --------------------------------------------------
# Check Whether Query Is In Scope
# --------------------------------------------------

def is_query_in_scope(query):
    """
    Determine whether the query has sufficient
    similarity with the knowledge base.
    """

    best_document = get_best_document(query)

    return best_document is not None


# --------------------------------------------------
# RAG Answer Context
# --------------------------------------------------

def get_rag_context(query, top_k=3):
    """
    Return relevant documents that can be used
    as grounded context for generating an answer.
    """

    results = retrieve_documents(query, top_k=top_k)

    relevant_results = [
        result
        for result in results
        if result["score"] >= RETRIEVAL_THRESHOLD
    ]

    return relevant_results


# --------------------------------------------------
# Test the Retriever
# --------------------------------------------------

if __name__ == "__main__":

    test_queries = [
        "I forgot my password",
        "How do I change my credit card?",
        "The dashboard is not loading",
        "What is the API rate limit?",
        "Can you recommend a movie?"
    ]


    print("\nCustomer-Support-AI-Employee RAG Retriever")
    print("=" * 50)


    for query in test_queries:

        print(f"\nUser: {query}")

        results = retrieve_documents(query, top_k=2)

        if not results:
            print("No results found.")
            continue


        for result in results:

            print(
                f"  {result['id']} | "
                f"{result['title']} | "
                f"score={result['score']}"
            )