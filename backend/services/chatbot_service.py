"""
AI chatbot service powered by the Groq API.

The Groq API key and model name are read from environment variables
(loaded via python-dotenv in main.py). No secrets are hardcoded.
"""

import os

import httpx

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are AgriAssist, a helpful AI farming assistant. Give clear, practical, "
    "and concise advice to farmers about crops, plant diseases, treatment, "
    "fertilizers, and general farming practices."
)


class ChatbotServiceError(Exception):
    """Raised when the chatbot service cannot produce a response."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


async def get_chat_response(user_message: str) -> str:
    """
    Send the user's message to the Groq chat completion API and return
    the assistant's reply text.
    """
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL")

    if not api_key:
        raise ChatbotServiceError("GROQ_API_KEY is not configured in the environment.")
    if not model:
        raise ChatbotServiceError("GROQ_MODEL is not configured in the environment.")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.6,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(GROQ_API_URL, json=payload, headers=headers)
    except httpx.RequestError as exc:
        raise ChatbotServiceError(f"Could not reach Groq API: {exc}") from exc

    if response.status_code != 200:
        raise ChatbotServiceError(
            f"Groq API returned an error (status {response.status_code}): {response.text}"
        )

    data = response.json()

    try:
        reply = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ChatbotServiceError("Groq API response was in an unexpected format.") from exc

    return reply.strip()
