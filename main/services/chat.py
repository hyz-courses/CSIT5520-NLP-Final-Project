"""
A tool functionality to simply forward
SSE messages streamed from dify.
"""

import httpx
from proj.context import get_project_context
from main.dao import ChatRequest

root, env = get_project_context()

ERR_JSON_SSE = 'data: {"event": "error", "message": "{message}"}\n\n'

async def dify_stream_generator(request: ChatRequest):
    """
    Yield SSE message from time to time.
    """

    async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
        try:
            async with client.stream(
                method="POST",
                url=env.DIFY_API_URL,
                headers={
                    "Authorization": f"Bearer {env.DIFY_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=request.model_dump(mode="json"),
            ) as response:

                if response.status_code != 200:
                    error_text = await response.aread()
                    yield ERR_JSON_SSE.format(message=error_text.decode())
                    return

                async for sse_line in response.aiter_lines():
                    sse_line = sse_line.strip()

                    if (
                        not sse_line
                        or sse_line.startswith("event:")
                        or not sse_line.startswith("data:")
                    ):
                        continue

                    yield f"{sse_line}\n\n"

        except httpx.RequestError as e:
            yield ERR_JSON_SSE.format(message=f"Connection Error: {str(e)}")
