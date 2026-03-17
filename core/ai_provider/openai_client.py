from openai import OpenAI, AsyncOpenAI

from proj.context import get_project_context

root, env = get_project_context()


def get_client() -> OpenAI:
    return OpenAI(api_key=env.QWEN_API_KEY, base_url=env.ALICLOUD_BASE_URL)


def get_async_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=env.QWEN_API_KEY, base_url=env.ALICLOUD_BASE_URL)
