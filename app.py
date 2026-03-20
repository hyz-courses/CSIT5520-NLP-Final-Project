"""
Main facade of backend.
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from main.services.chat import dify_stream_generator
from main.dao import ChatRequest

app = FastAPI()


@app.post("/chat")
async def chat_stream(request: ChatRequest):
    """
    Returns stream of SSE message to frontend.
    """

    return StreamingResponse(
        dify_stream_generator(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@app.get("/are-you-still-there")
async def health():
    """
    Health check for debugging.

    https://www.youtube.com/watch?v=Y6ljFaKRTrI
    """
    
    return {"status": "still-alive"}