from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from ..services.claude_service import ClaudeService

router = APIRouter()
claude_service = ClaudeService()

class TaskConfig(BaseModel):
    name: str
    description: str
    strategy: str
    tags: list[str]

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    role: str
    content: str
    chat_id: str

@router.post("/chat/start")
async def start_chat(task_config: TaskConfig) -> Dict[str, str]:
    """Start a new chat session with Claude"""
    try:
        chat_id = claude_service.create_chat(task_config.dict())
        return {"chat_id": chat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/{chat_id}/message")
async def send_message(chat_id: str, message: ChatMessage) -> ChatResponse:
    """Send a message to an existing chat session"""
    try:
        response = claude_service.send_message(chat_id, message.message)
        return ChatResponse(**response)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
