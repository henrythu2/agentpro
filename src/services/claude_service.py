import os
from typing import Dict, Optional
import anthropic
from ..tasks.order_cancellation.models import Order

class ClaudeService:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv('CLAUDE_API_KEY')
        )
        self.model = "claude-3-opus-20240229"
        self.active_chats: Dict[str, str] = {}  # chatId -> thread_id mapping

    def create_chat(self, task_config: dict) -> str:
        """Create a new chat session with Claude"""
        system_prompt = f"""You are a task agent configured with the following parameters:
Task Name: {task_config['name']}
Description: {task_config['description']}
Strategy: {task_config['strategy']}

Follow the strategy exactly as specified when interacting with users."""

        message = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            max_tokens=4096,
            messages=[
                {
                    "role": "assistant",
                    "content": "I am ready to help you with your task. How can I assist you today?"
                }
            ]
        )
        
        chat_id = message.id
        self.active_chats[chat_id] = message.thread_id
        return chat_id

    def send_message(self, chat_id: str, message: str) -> dict:
        """Send a message to an existing chat session"""
        if chat_id not in self.active_chats:
            raise ValueError("Invalid chat ID")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            thread_id=self.active_chats[chat_id]
        )

        return {
            "role": "assistant",
            "content": response.content[0].text,
            "chat_id": chat_id
        }
