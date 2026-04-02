import os
import logging
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


def setup_logger(name: str = "CSIT5520") -> logging.Logger:
    """
    Configure logger to write to resources/errlogs directory.
    
    Args:
        name: Logger name, defaults to "CSIT5520"
    
    Returns:
        Configured logger instance
    """
    root = get_project_root()
    log_dir = root / "resources" / "errlogs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # File handler
    log_file = log_dir / "app.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(file_handler)
    
    return logger


# Global logger instance - initialized once at module load
logger = setup_logger()