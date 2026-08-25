import React from "react";
import {
    Sparkles,
    User,
    BookOpen,
    AlertTriangle,
    Info,
    CheckCircle2
} from "lucide-react";
import EscalationCard from "./EscalationCard";


function Message({ message }) {

    const isUser = message.role === "user";


    // --------------------------------------------------
    // Format Confidence
    // --------------------------------------------------

    function formatConfidence(value) {

        if (
            value === undefined ||
            value === null
        ) {
            return null;
        }

        return `${Math.round(value * 100)}%`;
    }


    // --------------------------------------------------
    // Assistant Message
    // --------------------------------------------------

    if (!isUser) {

        return (

            <div
                className={`message-row assistant-row ${
                    message.type || ""
                }`}
            >

                {/* Assistant Avatar */}

                <div className="avatar assistant-avatar">

                    <Sparkles size={16} />

                </div>


                {/* Message Content */}

                <div className="assistant-message-wrapper">

                    {/* Main Message Bubble */}

                    <div
                        className={`message-bubble assistant-bubble ${
                            message.type || ""
                        }`}
                    >

                        {/* Icon for special messages */}

                        {message.type === "clarification" && (

                            <div className="message-type-icon">

                                <Info size={16} />

                            </div>

                        )}


                        {message.type === "error" && (

                            <div className="message-type-icon error-icon">

                                <AlertTriangle size={16} />

                            </div>

                        )}


                        <div
                            className="message-content"
                            dangerouslySetInnerHTML={{
                                __html: message.content
                            }}
                        />

                    </div>


                    {/* ==================================
                        Source Information
                    =================================== */}

                    {message.source && (

                        <div className="source-card">

                            <div className="source-icon">

                                <BookOpen size={15} />

                            </div>

                            <div className="source-details">

                                <span className="source-label">
                                    Knowledge Base
                                </span>

                                <strong>
                                    {message.source.id}
                                </strong>

                                <span>
                                    {message.source.title}
                                </span>

                            </div>

                        </div>

                    )}


                    {/* ==================================
                        Confidence Information
                    =================================== */}

                    {message.classificationConfidence !==
                        undefined && (

                        <div className="confidence-card">

                            <div className="confidence-header">

                                <span>
                                    AI confidence
                                </span>

                                {message.type === "normal" && (

                                    <CheckCircle2
                                        size={14}
                                    />

                                )}

                            </div>


                            <div className="confidence-values">

                                <div>

                                    <span>
                                        Category
                                    </span>

                                    <strong>
                                        {formatConfidence(
                                            message.classificationConfidence
                                        )}
                                    </strong>

                                </div>


                                <div>

                                    <span>
                                        Knowledge base
                                    </span>

                                    <strong>
                                        {formatConfidence(
                                            message.retrievalConfidence
                                        )}
                                    </strong>

                                </div>

                            </div>

                        </div>

                    )}


                    {/* ==================================
                        Category
                    =================================== */}

                    {message.category && (

                        <div className="category-tag">

                            Category:

                            <strong>
                                {formatCategory(
                                    message.category
                                )}
                            </strong>

                        </div>

                    )}


                    {/* ==================================
                        Escalation
                    =================================== */}

                    {message.escalated && (

                        <EscalationCard
                            ticket={message.ticket}
                            reason={message.reason}
                            reasonCode={message.reasonCode}
                        />

                    )}


                    {/* Timestamp */}

                    <div className="message-time">

                        {message.time}

                    </div>

                </div>

            </div>
        );
    }


    // --------------------------------------------------
    // User Message
    // --------------------------------------------------

    return (

        <div className="message-row user-row">

            <div className="user-message-wrapper">

                <div className="message-bubble user-bubble">

                    <div className="message-content">

                        {message.content}

                    </div>

                </div>


                <div className="message-time user-time">

                    {message.time}

                </div>

            </div>


            <div className="avatar user-avatar">

                <User size={16} />

            </div>

        </div>
    );
}


// --------------------------------------------------
// Category Formatting
// --------------------------------------------------

function formatCategory(category) {

    if (!category) {
        return "Unknown";
    }


    return category
        .replace(/_/g, " ")
        .replace(/\b\w/g, character =>
            character.toUpperCase()
        );
}


export default Message;