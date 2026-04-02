import os
from typing import Tuple
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Env:
    """Environment variables for the project."""
    QWEN_API_KEY: str
    ALICLOUD_BASE_URL: str
    QWEN_TEXT_EMBED_MODEL: str
    DIFY_API_URL: str
    DIFY_API_KEY: str
    MAX_FILE_SIZE_MB: int 
    MILVUS_URI: str
    MILVUS_COLLECTION: str
    MILVUS_TOKEN: str

    def __init__(self):
        load_dotenv(Path.joinpath(get_project_root(), "resources", ".env"))

        for field in self.__dataclass_fields__:
            if os.getenv(field) is None:
                raise ValueError(f"Environment variable '{field}' is not set.")
            setattr(self, field, os.getenv(field))


def get_project_root() -> Path:
    """Returns the root path of the project."""

    return Path(__file__).parent.parent


def get_project_context() -> Tuple[Path, Env]:
    """Returns the project root path and environment variables."""
    return get_project_root(), Env()