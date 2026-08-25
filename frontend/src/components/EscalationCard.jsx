import React from "react";
import {
    AlertTriangle,
    UserRound,
    Ticket,
    ArrowUpRight
} from "lucide-react";
function EscalationCard({
    ticket,
    reason,
    reasonCode
}) {

    // --------------------------------------------------
    // Format Escalation Reason
    // --------------------------------------------------

    function formatReasonCode(code) {

        if (!code) {
            return "Human review required";
        }

        return code
            .replace(/_/g, " ")
            .toLowerCase()
            .replace(/\b\w/g, character =>
                character.toUpperCase()
            );
    }


    return (

        <div className="escalation-card">

            {/* =========================================
                Header
            ========================================== */}

            <div className="escalation-header">

                <div className="escalation-icon">

                    <AlertTriangle size={18} />

                </div>


                <div className="escalation-title">

                    <strong>
                        Human Support Escalation
                    </strong>

                    <span>
                        Human review recommended
                    </span>

                </div>

            </div>


            {/* =========================================
                Reason
            ========================================== */}

            <div className="escalation-reason">

                <div className="escalation-label">

                    <AlertTriangle size={14} />

                    <span>
                        Why was this escalated?
                    </span>

                </div>


                <p>
                    {reason ||
                        "The chatbot could not confidently answer the request."
                    }
                </p>

            </div>


            {/* =========================================
                Reason Code
            ========================================== */}

            {reasonCode && (

                <div className="reason-code">

                    <span>
                        Decision
                    </span>

                    <strong>
                        {formatReasonCode(
                            reasonCode
                        )}
                    </strong>

                </div>

            )}


            {/* =========================================
                Ticket Information
            ========================================== */}

            {ticket && (

                <div className="ticket-details">

                    <div className="ticket-item">

                        <Ticket size={15} />

                        <div>

                            <span>
                                Support Ticket
                            </span>

                            <strong>
                                {ticket.id}
                            </strong>

                        </div>

                    </div>


                    <div className="ticket-item">

                        <UserRound size={15} />

                        <div>

                            <span>
                                Status
                            </span>

                            <strong>
                                {formatStatus(
                                    ticket.status
                                )}
                            </strong>

                        </div>

                    </div>

                </div>

            )}


            {/* =========================================
                Human Review Notice
            ========================================== */}

            <div className="human-review-notice">

                <div className="review-icon">

                    <ArrowUpRight size={15} />

                </div>


                <span>

                    Your request has been marked for
                    human review. The assistant has not
                    provided an unsupported answer.

                </span>

            </div>

        </div>
    );
}


// --------------------------------------------------
// Format Ticket Status
// --------------------------------------------------

function formatStatus(status) {

    if (!status) {
        return "Human Review";
    }


    return status
        .replace(/_/g, " ")
        .replace(/\b\w/g, character =>
            character.toUpperCase()
        );
}


export default EscalationCard;