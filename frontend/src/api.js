// --------------------------------------------------
// Customer-Support-AI-Employee
// API Service
// --------------------------------------------------

// Flask backend URL, configurable for local and deployed environments.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";


// --------------------------------------------------
// Send Chat Message
// --------------------------------------------------

export async function sendChatMessage(message) {

    const response = await fetch(
        `${API_BASE_URL}/api/chat`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        }
    );


    // ----------------------------------------------
    // Handle HTTP Errors
    // ----------------------------------------------

    if (!response.ok) {

        let errorMessage =
            "Unable to communicate with the support server.";

        try {

            const errorData =
                await response.json();

            if (errorData.error) {
                errorMessage = errorData.error;
            }

        } catch {
            // Ignore JSON parsing errors
        }


        throw new Error(errorMessage);
    }


    // ----------------------------------------------
    // Parse JSON Response
    // ----------------------------------------------

    const data = await response.json();


    // ----------------------------------------------
    // Validate API Response
    // ----------------------------------------------

    if (!data.success) {

        throw new Error(
            data.error ||
            "The support service returned an invalid response."
        );
    }


    return data;
}


// --------------------------------------------------
// Check Backend Health
// --------------------------------------------------

export async function checkBackendHealth() {

    const response = await fetch(
        `${API_BASE_URL}/api/health`
    );


    if (!response.ok) {
        throw new Error(
            "Backend health check failed."
        );
    }


    return await response.json();
}