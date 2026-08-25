"""
Customer-Support-AI-Employee
Main Flask API

Responsibilities:
- Receive chat messages
- Classify support tickets
- Retrieve relevant FAQ documents
- Apply escalation logic
- Return grounded responses
"""


from flask import Flask, request, jsonify
from flask_cors import CORS

from classifier import classify_ticket
from rag import get_rag_context
from escalation import (
    evaluate_query,
    build_escalation_message
)


# --------------------------------------------------
# Flask Application
# --------------------------------------------------

app = Flask(__name__)

# Allow the React frontend to communicate with
# the Flask backend during local development.
CORS(app)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

APP_NAME = "Customer-Support-AI-Employee"
APP_VERSION = "1.0.0"


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Check whether the backend is running.
    """

    return jsonify({
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION
    })


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chatbot endpoint.

    Expected request:

    {
        "message": "I forgot my password"
    }
    """

    # ----------------------------------------------
    # Validate Request
    # ----------------------------------------------

    data = request.get_json(silent=True)


    if not data:

        return jsonify({
            "success": False,
            "error": "Request body must contain JSON."
        }), 400


    message = data.get("message", "")


    if not isinstance(message, str):

        return jsonify({
            "success": False,
            "error": "Message must be a string."
        }), 400


    message = message.strip()


    if not message:

        return jsonify({
            "success": False,
            "error": "Message cannot be empty."
        }), 400


    # ----------------------------------------------
    # Step 1: Classify Ticket
    # ----------------------------------------------

    classification = classify_ticket(message)


    # ----------------------------------------------
    # Step 2: Retrieve Relevant Documents
    # ----------------------------------------------

    retrieval_results = get_rag_context(
        message,
        top_k=3
    )


    # ----------------------------------------------
    # Step 3: Evaluate Confidence
    # ----------------------------------------------

    decision = evaluate_query(
        classification,
        retrieval_results
    )


    # ----------------------------------------------
    # Step 4: Generate Response
    # ----------------------------------------------

    action = decision["action"]


    # ----------------------------------------------
    # ANSWER
    # ----------------------------------------------

    if action == "answer":

        best_document = retrieval_results[0]


        response_message = (
            best_document["content"]
        )


        return jsonify({

            "success": True,

            "action": "answer",

            "message": response_message,

            "category":
                classification["category"],

            "classification_confidence":
                classification["confidence"],

            "retrieval_confidence":
                best_document["score"],

            "source": {
                "id": best_document["id"],
                "title": best_document["title"]
            },

            "reason": decision["reason"],

            "escalated": False

        })


    # ----------------------------------------------
    # CLARIFICATION
    # ----------------------------------------------

    if action == "clarify":

        category = classification["category"]


        if category == "billing":

            clarification_message = (
                "Could you provide a little more detail "
                "about the billing issue? For example, "
                "are you asking about a payment, invoice, "
                "refund, or subscription?"
            )


        elif category == "technical":

            clarification_message = (
                "Could you describe the technical problem "
                "in a little more detail? For example, "
                "is a page not loading, are you seeing an "
                "error, or is an integration not working?"
            )


        elif category == "account_access":

            clarification_message = (
                "Could you tell me more about the account "
                "access problem? For example, are you "
                "having trouble logging in, resetting your "
                "password, or completing verification?"
            )


        else:

            clarification_message = (
                "Could you provide a little more information "
                "about the problem so I can determine how "
                "best to help?"
            )


        return jsonify({

            "success": True,

            "action": "clarify",

            "message":
                clarification_message,

            "category":
                classification["category"],

            "classification_confidence":
                classification["confidence"],

            "retrieval_confidence":
                decision["retrieval_confidence"],

            "source": None,

            "reason":
                decision["reason"],

            "escalated": False

        })


    # ----------------------------------------------
    # ESCALATION
    # ----------------------------------------------

    if action == "escalate":

        escalation_message = (
            build_escalation_message(
                decision
            )
        )


        # Synthetic ticket ID.
        # In a real application this would be
        # generated by a support/ticketing system.
        ticket_id = create_ticket_id()


        return jsonify({

            "success": True,

            "action": "escalate",

            "message":
                escalation_message,

            "category":
                classification["category"],

            "classification_confidence":
                classification["confidence"],

            "retrieval_confidence":
                decision["retrieval_confidence"],

            "source": None,

            "reason":
                decision["reason"],

            "reason_code":
                decision["reason_code"],

            "escalated": True,

            "ticket": {
                "id": ticket_id,
                "status": "human_review",
                "category":
                    classification["category"]
            }

        })


    # ----------------------------------------------
    # Safety Fallback
    # ----------------------------------------------

    return jsonify({

        "success": False,

        "error": (
            "The chatbot could not determine "
            "how to handle this request."
        )

    }), 500


# --------------------------------------------------
# Synthetic Ticket ID Generator
# --------------------------------------------------

def create_ticket_id():
    """
    Generate a synthetic support ticket ID.

    Example:
        CD-20260825-4821
    """

    from datetime import datetime
    import random


    timestamp = datetime.now().strftime(
        "%Y%m%d"
    )

    random_number = random.randint(
        1000,
        9999
    )


    return f"CD-{timestamp}-{random_number}"


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("Customer-Support-AI-Employee")
    print("=" * 55)
    print("API running at:")
    print("http://127.0.0.1:5000")
    print()
    print("Health check:")
    print("http://127.0.0.1:5000/api/health")
    print("=" * 55)


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )