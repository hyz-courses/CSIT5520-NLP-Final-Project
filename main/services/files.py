from typing import List

from pymilvus import MilvusClient

from proj.context import get_project_context, logger
from core.embed import embed_text
from main.obj.dao import Chunk, DBRecord
from core.obj.dao import TextEmbeddingList
from main.obj.errors import InvalidFileTypeError, OutboundNetworkError

root, env = get_project_context()

async def write_milvus_record(db_records: List[DBRecord]) -> int:
    """
    Given a list of database records, store them into Milvus.

    Args:
        db_records: A list of DBRecord objects to be stored in Milvus.
    """

    client = MilvusClient(uri=env.MILVUS_URI, token=env.MILVUS_TOKEN)
    if client is None:
        raise OutboundNetworkError("Milvus client not connected. Please start Milvus server.")
    
    insert_data = [db_record.model_dump(mode="python") for db_record in db_records]    

    res = client.insert(collection_name=env.MILVUS_COLLECTION, data=insert_data)

    return res["insert_count"]


async def store_chunks(chunk_list: List[Chunk]) -> int:
    """
    Generate the embedding for this file.
    If any failure is met, return None

    Args:
        text_list: The list of text strings to be embedded.

    Returns:
        TextEmbeddingList: The list of wrapped text embeddings.
    """

    try:

        # From given chunk list, get list of embedding vectors
        text_list = [chunk.text for chunk in chunk_list]
        text_emb_list = await embed_text(input_list=text_list)
        emb_list = text_emb_list.embeddings

        # Compress the chunk list and embedding list into a list of
        # database records.
        db_records = [
            DBRecord(**chunk.model_dump(mode="python"), vector=emb)
            for (chunk, emb) in zip(chunk_list, emb_list)
        ]

        effected_rows = await write_milvus_record(db_records)
        return effected_rows
    except Exception as e:
        logger.error(f"Error occurred while storing chunks: {e}.")
        return -1
