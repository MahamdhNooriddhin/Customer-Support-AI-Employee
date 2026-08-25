import React from "react";
import Message from "./Message";

import {
    Send,
    Sparkles,
    ShieldCheck,
    CircleHelp
} from "lucide-react";


function ChatWindow({
    messages,
    input,
    setInput,
    isLoading,
    onSend,
    onKeyDown,
    quickActions
}) {

    return (

        <div className="chat-page">

            {/* =========================================
                Main Chat Container
            ========================================== */}

            <div className="chat-container">


                {/* =====================================
                    Header
                ====================================== */}

                <header className="chat-header">

                    <div className="brand-section">

                        <div className="brand-icon">
                            <Sparkles size={22} />
                        </div>

                        <div className="brand-info">

                            <h1>
                                CloudDesk
                            </h1>

                            <span>
                                AI Support Assistant
                            </span>

                        </div>

                    </div>


                    <div className="online-status">

                        <span className="status-dot"></span>

                        <span>
                            Online
                        </span>

                    </div>

                </header>


                {/* =====================================
                    Trust / Information Bar
                ====================================== */}

                <div className="info-bar">

                    <div className="info-item">

                        <ShieldCheck size={16} />

                        <span>
                            Answers are grounded in CloudDesk documentation
                        </span>

                    </div>

                    <div className="info-item">

                        <CircleHelp size={16} />

                        <span>
                            Human support available when needed
                        </span>

                    </div>

                </div>


                {/* =====================================
                    Messages
                ====================================== */}

                <main className="messages-area">

                    {messages.map(message => (

                        <Message
                            key={message.id}
                            message={message}
                        />

                    ))}


                    {/* =================================
                        Loading Indicator
                    ================================== */}

                    {isLoading && (

                        <div className="typing-row">

                            <div className="avatar assistant-avatar">
                                <Sparkles size={16} />
                            </div>

                            <div className="typing-bubble">

                                <span></span>
                                <span></span>
                                <span></span>

                            </div>

                        </div>

                    )}

                </main>


                {/* =====================================
                    Quick Actions
                ====================================== */}

                {!isLoading && messages.length <= 2 && (

                    <div className="quick-actions">

                        <div className="quick-title">
                            Common questions
                        </div>

                        <div className="quick-buttons">

                            {quickActions.map(
                                (action, index) => (

                                    <button
                                        key={index}
                                        className="quick-button"
                                        onClick={() =>
                                            onSend(
                                                action.message
                                            )
                                        }
                                    >
                                        {action.label}
                                    </button>

                                )
                            )}

                        </div>

                    </div>

                )}


                {/* =====================================
                    Input Area
                ====================================== */}

                <div className="input-section">

                    <div className="input-wrapper">

                        <textarea
                            value={input}
                            onChange={(event) =>
                                setInput(
                                    event.target.value
                                )
                            }
                            onKeyDown={onKeyDown}
                            placeholder="Describe your issue..."
                            rows={1}
                            disabled={isLoading}
                        />


                        <button
                            className="send-button"
                            onClick={() => onSend()}
                            disabled={
                                !input.trim() ||
                                isLoading
                            }
                            aria-label="Send message"
                        >

                            <Send size={18} />

                        </button>

                    </div>


                    <div className="input-footer">

                        <span>
                            Press Enter to send
                        </span>

                        <span>
                            CloudDesk Support
                        </span>

                    </div>

                </div>

            </div>

        </div>
    );
}


export default ChatWindow;