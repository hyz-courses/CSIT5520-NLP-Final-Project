from openai import OpenAI

from proj.context import get_project_context

root, env = get_project_context()


def get_client() -> OpenAI:
    return OpenAI(api_key=env.QWEN_API_KEY, base_url=env.ALICLOUD_BASE_URL)
