"""
Data object model during requests.
"""

from typing import List

from fastapi import File, UploadFile
from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    user: str = "default-user"
    conversation_id: str | None = None
    inputs: dict = {}
    response_mode: str = "streaming"


class FileUploadRequest(BaseModel):
    token: str
    files: List[UploadFile] = File(...)