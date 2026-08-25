import React, { useState } from "react";

import ChatWindow from "./components/ChatWindow";
import { sendChatMessage } from "./api";


function App() {

    // --------------------------------------------------
    // Chat Messages
    // --------------------------------------------------

    const [messages, setMessages] = useState([
        {
            id: 1,
            role: "assistant",
            content:
                "Hi! I'm CloudDesk's AI Support Assistant. I can help with billing, technical issues, and account access.",
            type: "normal",
            time: getCurrentTime()
        }
    ]);


    // --------------------------------------------------
    // Input State
    // --------------------------------------------------

    const [input, setInput] = useState("");


    // --------------------------------------------------
    // Loading State
    // --------------------------------------------------

    const [isLoading, setIsLoading] = useState(false);


    // --------------------------------------------------
    // Send Message
    // --------------------------------------------------

    async function handleSendMessage(messageFromQuickAction = null) {

        const message =
            messageFromQuickAction !== null
                ? messageFromQuickAction
                : input.trim();


        // Don't send empty messages
        if (!message || isLoading) {
            return;
        }


        // ----------------------------------------------
        // Add User Message
        // ----------------------------------------------

        const userMessage = {
            id: Date.now(),
            role: "user",
            content: message,
            type: "normal",
            time: getCurrentTime()
        };


        setMessages(previousMessages => [
            ...previousMessages,
            userMessage
        ]);


        setInput("");
        setIsLoading(true);


        try {

            // ------------------------------------------
            // Send Request To Flask Backend
            // ------------------------------------------

            const response = await sendChatMessage(
                message
            );


            // ------------------------------------------
            // Create Assistant Message
            // ------------------------------------------

            const assistantMessage = {
                id: Date.now() + 1,

                role: "assistant",

                content:
                    response.message,

                type:
                    response.action === "escalate"
                        ? "escalation"
                        : response.action === "clarify"
                            ? "clarification"
                            : "normal",

                category:
                    response.category,

                classificationConfidence:
                    response.classification_confidence,

                retrievalConfidence:
                    response.retrieval_confidence,

                source:
                    response.source,

                reason:
                    response.reason,

                reasonCode:
                    response.reason_code,

                escalated:
                    response.escalated,

                ticket:
                    response.ticket,

                time:
                    getCurrentTime()
            };


            setMessages(previousMessages => [
                ...previousMessages,
                assistantMessage
            ]);

        } catch (error) {

            // ------------------------------------------
            // API Error
            // ------------------------------------------

            console.error(
                "Chat API error:",
                error
            );


            const errorMessage = {
                id: Date.now() + 1,

                role: "assistant",

                content:
                    "I'm unable to connect to the CloudDesk support service right now. Please make sure the backend server is running and try again.",

                type: "error",

                time: getCurrentTime()
            };


            setMessages(previousMessages => [
                ...previousMessages,
                errorMessage
            ]);

        } finally {

            setIsLoading(false);

        }
    }


    // --------------------------------------------------
    // Handle Enter Key
    // --------------------------------------------------

    function handleKeyDown(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            handleSendMessage();

        }

    }


    // --------------------------------------------------
    // Quick Actions
    // --------------------------------------------------

    const quickActions = [

        {
            label: "Reset my password",
            message:
                "I forgot my password. How can I reset it?"
        },

        {
            label: "Billing help",
            message:
                "How do I update my payment method?"
        },

        {
            label: "Dashboard problem",
            message:
                "The CloudDesk dashboard is not loading."
        },

        {
            label: "API help",
            message:
                "How do I authenticate with the CloudDesk API?"
        }

    ];


    // --------------------------------------------------
    // Render
    // --------------------------------------------------

    return (

        <div className="app">

            <ChatWindow

                messages={messages}

                input={input}

                setInput={setInput}

                isLoading={isLoading}

                onSend={handleSendMessage}

                onKeyDown={handleKeyDown}

                quickActions={quickActions}

            />

        </div>

    );
}


// --------------------------------------------------
// Current Time Helper
// --------------------------------------------------

function getCurrentTime() {

    return new Date().toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );

}


export default App;