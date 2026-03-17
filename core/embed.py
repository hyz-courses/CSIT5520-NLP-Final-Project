from typing import List
from core.ai_provider.openai_client import get_client
from proj.context import get_project_context
from core.obj.dao import TextEmbeddingList

root, env = get_project_context()


def embed_text(input_list: List[str]):
    client = get_client()

    completion = client.embeddings.create(
        model=env.QWEN_TEXT_EMBED_MODEL, input=input_list
    )

    return TextEmbeddingList(input_list, completion)


if __name__ == "__main__":
    # for testing only
    print(
        embed_text(
            [
                "The rusty gate creaked loudly every time the wind blew.",
                "She decided to plant lavender in her garden to attract bees.",
                "Technology has fundamentally changed the way we communicate with one another.",
                "The chef added a pinch of sea salt to enhance the flavor of the soup.",
                "Finding a quiet spot in the city can be quite a challenge during rush hour.",
                "The old bookstore smelled of vanilla and aged paper.",
                "He forgot his umbrella and got soaked during the sudden downpour.",
                "Learning a new language opens up many opportunities for travel and work.",
                "The cat spent the entire afternoon napping in a patch of sunlight.",
                "We should always strive to be kind to everyone we meet.",
            ]
        )
    )
