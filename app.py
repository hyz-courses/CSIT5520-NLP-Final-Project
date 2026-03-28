"""
Main facade of backend.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse

from main.services.chat import dify_stream_generator
from main.services.files import embed_files
from main.dao import ChatRequest, FileUploadRequest
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


@app.post("/doc")
async def doc_upload(request: FileUploadRequest):
    try:
        num_files = await embed_files(request.files)
        return {"success": True, "num_files": num_files}
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