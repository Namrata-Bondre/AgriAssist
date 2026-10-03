"""AI chatbot endpoint (Groq-powered)."""

from fastapi import APIRouter, HTTPException, status

from backend.schemas.chatbot import ChatRequest, ChatResponse
from backend.services.chatbot_service import ChatbotServiceError, get_chat_response

router = APIRouter(prefix="/api", tags=["Chatbot"])


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(payload: ChatRequest) -> ChatResponse:
    """Send a message to the AI chatbot and return its response."""
    if not payload.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty.",
        )

    try:
        reply = await get_chat_response(payload.message)
    except ChatbotServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.message,
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chatbot request failed: {exc}",
        ) from exc

    return ChatResponse(success=True, response=reply)
