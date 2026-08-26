const API_URL =
    import.meta.env.VITE_API_URL ||
    "https://customer-support-ai-employee-d5jj.onrender.com";


export async function sendMessage(message) {

    try {

        console.log("Sending request to:", `${API_URL}/api/chat`);

        const response = await fetch(
            `${API_URL}/api/chat`,
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


        if (!response.ok) {

            const errorText = await response.text();

            console.error(
                "Backend response:",
                response.status,
                errorText
            );

            throw new Error(
                `Backend returned ${response.status}`
            );
        }


        const data = await response.json();

        console.log("Chat API response:", data);

        return data;

    } catch (error) {

        console.error(
            "Chat API error:",
            error
        );

        throw error;
    }
}