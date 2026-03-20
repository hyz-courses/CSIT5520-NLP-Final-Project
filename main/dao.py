"""
Data object model during requests.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    user: str = "default-user"
    conversation_id: str | None = None
    inputs: dict = {}
    response_mode: str = "streaming"