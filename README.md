# Customer-Support-AI-Employee

Customer-Support-AI-Employee is an AI-powered customer support assistant built as a small full-stack demo application. It classifies incoming support requests, matches them against a support knowledge base, and decides whether to answer, ask a clarifying question, or escalate the issue to a human support team.

This project combines a Flask backend, a lightweight TF-IDF retrieval system, and a React frontend to simulate a practical support chatbot experience.

---

## Overview

The app is designed for a fictional SaaS product called CloudDesk. It helps users with common support needs such as:

- Billing and payment questions
- Technical issues and product errors
- Account access and login problems

It uses a rule-based decision pipeline:

1. User submits a message from the frontend.
2. The backend classifies the message into a category.
3. The retrieval layer searches the in-memory knowledge base for relevant FAQ articles.
4. The system decides if the query is answerable, needs clarification, or should be escalated.
5. The frontend displays the response in a chat interface.

---

## Features

### Ticket classification
The app classifies messages into:

- billing
- technical
- account_access
- unknown

This is implemented with a TF-IDF vectorizer and cosine similarity against synthetic training examples.

### Retrieval-augmented support answers
The app searches a curated knowledge base using TF-IDF similarity to find the most relevant support articles. This gives the assistant grounded responses based on the FAQ rather than free-form guessing.

### Escalation logic
If a request is outside the scope of the knowledge base or lacks enough confidence, the app will either:

- ask a follow-up clarification question, or
- escalate the request for human review

### Chat UI
The React frontend provides a simple support chat experience with quick actions such as:

- Reset my password
- Billing help
- Dashboard problem
- API help

---

## Technology Stack

### Backend
- Python
- Flask
- Flask-CORS
- scikit-learn
- NumPy
- SciPy

### Frontend
- React
- Vite
- JavaScript

---

## Project Structure

```text
Customer-Support-AI-Employee/
├── README.md
├── backend/
│   ├── app.py
│   ├── classifier.py
│   ├── escalation.py
│   ├── knowledge_base.json
│   ├── rag.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── api.js
│       ├── App.css
│       ├── App.jsx
│       ├── main.jsx
│       └── components/
│           ├── ChatWindow.jsx
│           ├── EscalationCard.jsx
│           └── Message.jsx
└── .gitignore
```

---

## How It Works

### 1. User input
A user sends a support question through the chat UI.

### 2. Classify the request
The backend runs `classify_ticket()` to assign a likely category.

### 3. Retrieve relevant content
The backend runs `get_rag_context()` to find top matching support documents from the knowledge base.

### 4. Evaluate the request
The escalation logic checks whether the answer is sufficiently relevant and confident.

### 5. Return a response
The system then returns one of the following:

- an answer from the knowledge base
- a clarification prompt
- an escalation message

---

## Knowledge Base

The knowledge base is stored in `backend/knowledge_base.json` and contains FAQ-style entries such as:

- Resetting your password
- Account locked after failed login attempts
- Two-factor authentication
- Updating payment information
- Understanding your invoice
- Canceling a subscription
- Refund policy
- Dashboard not loading
- API authentication
- API rate limits
- Browser compatibility
- Integration troubleshooting

These entries are used for grounded retrieval and answer generation.

---

## API Endpoints

### Health check

`GET /api/health`

Returns:

```json
{
  "status": "ok",
  "service": "Customer-Support-AI-Employee",
  "version": "1.0.0"
}
```

### Chat

`POST /api/chat`

Request body:

```json
{
  "message": "I forgot my password. How do I reset it?"
}
```

Example successful response:

```json
{
  "success": true,
  "action": "answer",
  "message": "If you forgot your CloudDesk password, go to the login page and select 'Forgot Password'. Enter your registered email address and CloudDesk will send you a password reset link.",
  "category": "account_access",
  "classification_confidence": 0.43,
  "retrieval_confidence": 0.54,
  "source": {
    "id": "KB-001",
    "title": "Resetting your password"
  },
  "reason": "Relevant knowledge base article matched the request.",
  "escalated": false
}
```

---

## Local Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### 1. Clone the repository

```bash
git clone <repository-url>
cd Customer-Support-AI-Employee
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask backend:

```bash
python app.py
```

The backend will run on:

```text
http://127.0.0.1:5000
```

### 3. Set up the frontend

Open a second terminal and run:

```bash
cd frontend
npm install
npm run dev
```

The Vite app usually runs at:

```text
http://127.0.0.1:5173
```

---

## Running the App

Once both servers are running:

1. Open the frontend in the browser.
2. Type a customer support question.
3. The app will classify the request, retrieve support articles, and respond accordingly.

Example queries:

- I forgot my password.
- How do I update my payment method?
- The dashboard is not loading.
- My API request is failing.
- My invoice looks incorrect.

---

## Example Behavior

### Example 1: Account access
Input:

```text
I forgot my password and cannot log in.
```

Likely output:

- category: account_access
- action: answer
- answer pulled from the reset password article

### Example 2: Billing question
Input:

```text
I need to change my credit card.
```

Likely output:

- category: billing
- action: answer
- answer pulled from the payment method article

### Example 3: Unknown or unclear request
Input:

```text
I need help with something unrelated to support.
```

Likely output:

- category: unknown
- action: clarify or escalate

---

## Notes on the Model

This project is intentionally lightweight and educational. It does not rely on a modern LLM or external AI service. Instead, it demonstrates a small retrieval-based support system using:

- TF-IDF text vectors
- cosine similarity
- rule-driven decision logic

This makes it easy to understand and modify for learning, demos, or prototype work.

---

## Customization Ideas

You can extend the project with:

- a real embedding model
- a database-backed knowledge base
- a production-grade ticketing workflow
- support for multilingual questions
- more robust escalation and logging
- authentication and user sessions

---

## Troubleshooting

### Backend not responding
Check that the Flask app is running:

```bash
cd backend
python app.py
```

### CORS issues
Ensure the frontend is contacting the backend at `http://127.0.0.1:5000` and that Flask-CORS is installed.

### Frontend not loading
Confirm dependencies are installed:

```bash
cd frontend
npm install
npm run dev
```

### Empty or poor responses
The knowledge base is intentionally small. Questions outside the supported support topics may trigger clarification or escalation.

---

## License

This project is provided for educational and demonstration purposes.

---

## Conclusion

Customer-Support-AI-Employee is a compact example of an AI-assisted customer support workflow. It demonstrates the flow of support triage, grounded retrieval, and escalation in a way that is easy to run locally and extend with additional features.
