from typing import List

from pathlib import Path
from fastapi import UploadFile

from proj.context import get_project_context
from core.embed import embed_text
from core.obj.dao import TextEmbeddingList
from main.obj.errors import InvalidFileTypeError, OutboundNetworkError

root, env = get_project_context()

def validate_file(file: UploadFile) -> bool:
    """
    Given a file, validate its file extension,
    mime type and size.

    Args:
        file: The uploaded file.
    
    Return:
        bool: Whether the file is valid.
    """
    
    if file.filename is None or file.size is None:
        return False

    # Validate File Type
    ext = Path(file.filename).suffix
    mime_type = file.content_type

    if ext != ".md" or mime_type != ".md":
        return False

    # Validate File Size
    if file.size > (env.MAX_FILE_SIZE_MB << 20):  # 20 MB
        return False
    
    return True


def parse_file(file: UploadFile) -> str:
    """
    Parse a single .md file into string.

    Args:
        file: The uploaded file.
    
    Returns:
        str: The returned parsed string from the file.
    """

    # TODO: Parse md files to text.
    
    return ""


async def embed_textlist(text_list: List[str]) -> TextEmbeddingList | None:
    """
    Generate the embedding for this file.
    If any failure is met, return None

    Args:
        text_list: The list of text strings to be embedded.
    
    Returns:
        TextEmbeddingList: The list of wrapped text embeddings.
    """
    
    try:
        text_emb_list = await embed_text(input_list=text_list)
        return text_emb_list
    except Exception:
        return None


async def embed_files(files: List[UploadFile]) -> int:
    """
    Organized pipeline of service.

    Args:
        files: The list of files.
    
    Returns:
        int: The number of files accepted.

    Raises:
        InvalidFileTypeError: One or more files has disallowed type.
        OutboundNetworkError: Having issue communicating with outbound service.
    """
    
    if any([not validate_file(file) for file in files]):
        raise InvalidFileTypeError(
            "One or more files has undesired extension or mime type.")

    # List of text embeddings
    text_emb_list = embed_textlist(text_list=[
        parse_file(file) for file in files])

    if text_emb_list is None:
        raise OutboundNetworkError(
            "Failed to communicate with the embedding service.")

    # TODO: storage

    return len(files)
    
    