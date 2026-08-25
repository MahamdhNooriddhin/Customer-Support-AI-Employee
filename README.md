# Customer-Support-AI-Employee

An AI-powered SaaS support chatbot that classifies incoming support
requests, retrieves answers from a small knowledge base, and escalates
low-confidence or out-of-scope requests to human support.

---

## 1. Project Overview

Customer-Support-AI-Employee is a fictional SaaS customer-support system.

The chatbot performs three main tasks:

1. Classifies incoming support messages.
2. Retrieves relevant information from a provided knowledge base.
3. Escalates requests when the system cannot confidently provide a
   grounded answer.

The system supports the following categories:

- Billing
- Technical
- Account Access

It also handles unknown and out-of-scope requests.

---

## 2. Main Features

### Ticket Classification

Incoming messages are classified into:

- `billing`
- `technical`
- `account_access`
- `unknown`

Example:

> "I need to update my credit card."

Classification:

```text
Category: billing