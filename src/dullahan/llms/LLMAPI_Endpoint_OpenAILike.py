from dotenv import load_dotenv
import os
import openai

from ..defs.botdef import IBotBase
from ..defs.datadef import ChatMessageData

class LLMAPI_OpenAILike(IBotBase):
    @classmethod
    def call(cls, model_name: str, endpoint: str, api_env_key: str, config: dict, messages: list[ChatMessageData]) -> str:
        # load secret key
        load_dotenv()
        api_key = os.getenv(api_env_key)

        # rebuild message
        messages = [
            {'role': mesg.role, 'content': mesg.message}
            for mesg in messages if mesg.role in ['system', 'user', 'assistant']]

        # pickup config
        kwargs = {}

        # call LLM API
        client = openai.OpenAI(api_key=api_key, base_url=endpoint)
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

