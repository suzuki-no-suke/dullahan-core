from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from ..defs.botdef import IBotBase
from ..defs.datadef import ChatMessageData

class LLMAPI_OpenAI(IBotBase):
    @classmethod
    def call(cls, model_name: str, config: dict, messages: list[ChatMessageData]) -> str:
        # rebuild message
        messages = [
            {'role': mesg.role, 'content': mesg.message}
            for mesg in messages if mesg.role in ['system', 'user', 'assistant']]
        
        # choose options
        kwargs = {}
        if 'temperature' in config:
            kwargs['temperature'] = config['temperature']

        # call LLM API
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
