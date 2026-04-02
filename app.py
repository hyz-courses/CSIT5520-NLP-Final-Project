"""
Main facade of backend.
"""

from typing import Optional

from fastapi import FastAPI, HTTPException, Header, status, Depends
from fastapi.responses import StreamingResponse

from main.services.chat import dify_stream_generator
from main.services.files import store_chunks
from main.obj.dao import ChatRequest, ChunkUploadRequest
from main.obj.errors import InvalidFileTypeError, OutboundNetworkError
from proj.context import get_project_context

root, env = get_project_context()

app = FastAPI()

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != env.DOCSEARCH_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid API Key")
    return x_api_key


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
async def chunk_upload(request: ChunkUploadRequest, _=Depends(verify_api_key)):
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