from typing import List
from dataclasses import dataclass
from openai.types import CreateEmbeddingResponse
from core.obj.errors import ResponseLengthMismatchError


@dataclass
class TextEmbeddingList:
    """
    A class wrapping a list of text documents and a
    list of embeddings. Elements are matched one-one
    using index.
    """
    
    texts: List[str]
    embeddings: List[List[float]]

    def __init__(
        self, texts: List[str], create_embedding_response: CreateEmbeddingResponse
    ):
        # Texts: RAG chunks, should have a length threshold.
        self.texts = texts

        # Embedding list
        data = create_embedding_response.data

        if len(texts) != len(data):
            raise ResponseLengthMismatchError(
                "The input texts length and the response data length does not match!"
            )

        data = sorted(data, key=lambda embedding: embedding.index)  # Sort by index

        embeddings = [data.embedding for data in data]  # Embedding literal value

        self.embeddings = embeddings

    def __str__(self):
        out = ""

        for text, emb_vector in zip(self.texts, self.embeddings):
            out += (
                f"\"{text[:15]}{'...' if len(text) > 15 else ''}\": "
                f"[{', '.join([f'{v: .18f}' for v in emb_vector[:4]])}, ..., {emb_vector[-1]: .18f}] "
                f"(length={len(emb_vector)})\n"
            )

        return out
