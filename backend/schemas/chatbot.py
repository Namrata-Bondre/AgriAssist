"""Pydantic schemas for the chatbot endpoint."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User's message to the assistant")


class ChatResponse(BaseModel):
    success: bool
    response: str
