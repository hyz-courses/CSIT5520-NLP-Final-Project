from typing import List

from core.ai_provider.openai_client import get_async_client
from proj.context import get_project_context
from core.obj.dao import TextEmbeddingList

root, env = get_project_context()


async def embed_text(input_list: List[str]):
    """
    Generate text embeddings using Qwen API asynchronously.
    The input list should be a list of text documents with
    pre-constrained length, e.g., 1024 tokens.
        
    Args:
        input_list: A list of text documents to be embedded.
    
    Returns:
        TextEmbeddingList: An object containing the original texts and their
            corresponding embeddings.
    
    Raises:
        ResponseLengthMismatchError: If the number of embeddings returned by
            the API does not match the number of input texts.
    """
    
    client = get_async_client()

    completion = await client.embeddings.create(
        model=env.QWEN_TEXT_EMBED_MODEL, input=input_list
    )

    return TextEmbeddingList(input_list, completion)

if __name__ == "__main__":
    import asyncio

    large_text = """
如果以电子形式寄送，则让学校通过加密方式把成绩单发送到pgdoc@ust.hk。注意，这里的加密方式指的是诸如港科大的区块链加密成绩单之类的加密方法，不是简单地发邮件附件。如果你的学校不知道什么叫加密方式，反过来询问你的话，可能是不具备这种方法，那么就需要使用实体寄送的形式。（注：其实这里说到底还是一个信任问题，往年也有同学所在的学校无法提供实体寄送，电子的也只能发邮件，在让科大相信这是学校官方的教务处邮箱以后，科大还是接受了发邮件附件的形式。总之发邮件不是一个首选，其他方法均不可行的话也可以试着与科大研究生院沟通、抄送原所在学校的教务机构，让学校与学校沟通确认。）
    """
    # for testing only
    print(
        asyncio.run(embed_text(
            [
                large_text,
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
        ))
    )