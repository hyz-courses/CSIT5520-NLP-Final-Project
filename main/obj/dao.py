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


class Chunk(BaseModel):
    original_filename: str
    title1: str
    title2: str | None
    text: str
    upload_time: str


class DBRecord(Chunk):
    # id: str
    vector: List[float]


class ChunkUploadRequest(BaseModel):
    chunks: List[Chunk]