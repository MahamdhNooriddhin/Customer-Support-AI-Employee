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

import os
import random
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from classifier import classify_ticket
from rag import get_rag_context
from escalation import (
    evaluate_query,
    build_escalation_message
)


# ============================================================
# Flask Application
# ============================================================

app = Flask(__name__)


# ============================================================
# CORS
# ============================================================

# Allow the React frontend to communicate with Flask.
#
# This is intentionally open for the assessment/demo.
# In production, restrict this to your frontend domain.

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*"
        }
    }
)


# ============================================================
# Configuration
# ============================================================

APP_NAME = "Customer-Support-AI-Employee"
APP_VERSION = "1.0.0"


# ============================================================
# Root Route
# ============================================================

@app.route("/", methods=["GET"])
def home():
    """
    Root endpoint.
    """

    return jsonify({
        "success": True,
        "service": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "message": "Customer Support AI Employee API is running."
    })


# ============================================================
# Health Check
# ============================================================

@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Health check endpoint used by Render and for debugging.
    """

    return jsonify({
        "success": True,
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION
    })


# ============================================================
# Chat Endpoint
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chatbot endpoint.

    Expected request:

    {
        "message": "I forgot my password"
    }
    """

    try:

        # ----------------------------------------------------
        # 1. Validate request
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # 2. Classify ticket
        # ----------------------------------------------------

        classification = classify_ticket(message)


        # ----------------------------------------------------
        # 3. Retrieve relevant knowledge-base documents
        # ----------------------------------------------------

        retrieval_results = get_rag_context(
            message,
            top_k=3
        )


        # Make sure retrieval results are usable.

        if retrieval_results is None:
            retrieval_results = []


        # ----------------------------------------------------
        # 4. Evaluate confidence / escalation
        # ----------------------------------------------------

        decision = evaluate_query(
            classification,
            retrieval_results
        )


        action = decision.get(
            "action",
            "escalate"
        )


        # ----------------------------------------------------
        # 5. ANSWER
        # ----------------------------------------------------

        if action == "answer":

            if not retrieval_results:

                return jsonify({

                    "success": True,

                    "action": "escalate",

                    "message": (
                        "I couldn't find a sufficiently relevant "
                        "answer in the CloudDesk knowledge base. "
                        "I'll escalate this request to a human "
                        "support agent."
                    ),

                    "category":
                        classification.get(
                            "category",
                            "unknown"
                        ),

                    "classification_confidence":
                        classification.get(
                            "confidence",
                            0
                        ),

                    "retrieval_confidence": 0,

                    "source": None,

                    "reason":
                        "No relevant knowledge-base document was found.",

                    "reason_code":
                        "NO_RETRIEVAL_RESULT",

                    "escalated": True,

                    "ticket": {
                        "id": create_ticket_id(),
                        "status": "human_review",
                        "category":
                            classification.get(
                                "category",
                                "unknown"
                            )
                    }

                })


            best_document = retrieval_results[0]


            response_message = best_document.get(
                "content",
                "I couldn't find an answer in the knowledge base."
            )


            return jsonify({

                "success": True,

                "action": "answer",

                "message": response_message,

                "category":
                    classification.get(
                        "category",
                        "unknown"
                    ),

                "classification_confidence":
                    classification.get(
                        "confidence",
                        0
                    ),

                "retrieval_confidence":
                    best_document.get(
                        "score",
                        0
                    ),

                "source": {
                    "id":
                        best_document.get(
                            "id",
                            "unknown"
                        ),

                    "title":
                        best_document.get(
                            "title",
                            "Knowledge Base"
                        )
                },

                "reason":
                    decision.get(
                        "reason",
                        "Answer found in the knowledge base."
                    ),

                "escalated": False

            })


        # ----------------------------------------------------
        # 6. CLARIFICATION
        # ----------------------------------------------------

        if action == "clarify":

            category = classification.get(
                "category",
                "unknown"
            )


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

                "message": clarification_message,

                "category":
                    classification.get(
                        "category",
                        "unknown"
                    ),

                "classification_confidence":
                    classification.get(
                        "confidence",
                        0
                    ),

                "retrieval_confidence":
                    decision.get(
                        "retrieval_confidence",
                        0
                    ),

                "source": None,

                "reason":
                    decision.get(
                        "reason",
                        "More information is required."
                    ),

                "escalated": False

            })


        # ----------------------------------------------------
        # 7. ESCALATION
        # ----------------------------------------------------

        if action == "escalate":

            escalation_message = build_escalation_message(
                decision
            )


            ticket_id = create_ticket_id()


            return jsonify({

                "success": True,

                "action": "escalate",

                "message": escalation_message,

                "category":
                    classification.get(
                        "category",
                        "unknown"
                    ),

                "classification_confidence":
                    classification.get(
                        "confidence",
                        0
                    ),

                "retrieval_confidence":
                    decision.get(
                        "retrieval_confidence",
                        0
                    ),

                "source": None,

                "reason":
                    decision.get(
                        "reason",
                        "Confidence was too low to provide a reliable answer."
                    ),

                "reason_code":
                    decision.get(
                        "reason_code",
                        "LOW_CONFIDENCE"
                    ),

                "escalated": True,

                "ticket": {

                    "id": ticket_id,

                    "status": "human_review",

                    "category":
                        classification.get(
                            "category",
                            "unknown"
                        )

                }

            })


        # ----------------------------------------------------
        # 8. Unknown action
        # ----------------------------------------------------

        return jsonify({

            "success": False,

            "action": "escalate",

            "message": (
                "I couldn't confidently determine how to "
                "handle your request, so I'm escalating it "
                "to a human support agent."
            ),

            "category":
                classification.get(
                    "category",
                    "unknown"
                ),

            "classification_confidence":
                classification.get(
                    "confidence",
                    0
                ),

            "retrieval_confidence":
                decision.get(
                    "retrieval_confidence",
                    0
                ),

            "source": None,

            "reason": (
                "The chatbot returned an unsupported "
                "decision and therefore used the safety fallback."
            ),

            "reason_code": "UNKNOWN_ACTION",

            "escalated": True,

            "ticket": {

                "id": create_ticket_id(),

                "status": "human_review",

                "category":
                    classification.get(
                        "category",
                        "unknown"
                    )

            }

        })


    except Exception as error:

        # ----------------------------------------------------
        # Unexpected server error
        # ----------------------------------------------------

        print(
            "CHAT API ERROR:",
            repr(error)
        )


        return jsonify({

            "success": False,

            "error": "Internal server error.",

            "message": (
                "I'm temporarily unable to process your "
                "request. Please try again or contact human "
                "support."
            )

        }), 500


# ============================================================
# Synthetic Ticket ID Generator
# ============================================================

def create_ticket_id():
    """
    Generate a synthetic support ticket ID.

    Example:
        CD-20260826-4821
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d"
    )


    random_number = random.randint(
        1000,
        9999
    )


    return f"CD-{timestamp}-{random_number}"


# ============================================================
# Error Handlers
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({

        "success": False,

        "error": "Endpoint not found.",

        "available_endpoints": [
            "/",
            "/api/health",
            "/api/chat"
        ]

    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({

        "success": False,

        "error": "HTTP method not allowed."

    }), 405


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    print()
    print("=" * 60)
    print(APP_NAME)
    print("=" * 60)
    print(f"Version: {APP_VERSION}")
    print(f"Port: {port}")
    print()
    print("Health:")
    print(f"http://127.0.0.1:{port}/api/health")
    print()
    print("Chat:")
    print(f"http://127.0.0.1:{port}/api/chat")
    print("=" * 60)


    app.run(

        host="0.0.0.0",

        port=port,

        debug=False

    )