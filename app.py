"""
Main facade of backend.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse

from main.services.chat import dify_stream_generator
from main.services.files import store_chunks
from main.obj.dao import ChatRequest, ChunkUploadRequest
from main.obj.errors import InvalidFileTypeError, OutboundNetworkError

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


@app.post("/chunk")
async def chunk_upload(request: ChunkUploadRequest):
    try:
        num_files = await store_chunks(request.chunks)
        return {"success": num_files != -1, "num_files": num_files}
    except InvalidFileTypeError | OutboundNetworkError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e)



@app.put("/doc")
async def doc_edit():
    pass


@app.delete("/doc")
async def doc_delete():
    pass


@app.get("/are-you-still-there")
async def health():
    """
    Health check for debugging.

    https://www.youtube.com/watch?v=Y6ljFaKRTrI
    """
    
    return {"status": "still-alive"}