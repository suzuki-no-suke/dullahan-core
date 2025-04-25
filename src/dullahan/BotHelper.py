from .defs.datadef import ChatMessageData
from jinja2 import Template

class BotHelper:
    def render_template(self, template: str, parameter: dict) -> str:
        jinja_template = Template(template)
        return jinja_template.render(**parameter)

    def llm_call(self, model_name: str, config: dict, messages: list[ChatMessageData]) -> str:
        if model_name in ["echo", "moch"]:
            from .llms.Functional_Echo import Functional_Echo
            return Functional_Echo.call(messages)
        elif model_name in ["gpt-4.1", "gpt-4o"]:
            from .llms.LLMAPI_OpenAI import LLMAPI_OpenAI
            return LLMAPI_OpenAI.call(model_name, config, messages)
        elif model_name in ['google/gemini-2.0-flash-001', 'deepseek/deepseek-v3-base:free']:
            from .llms.LLMAPI_Endpoint_OpenAILike import LLMAPI_OpenAILike
            return LLMAPI_OpenAILike.call(model_name, 'https://openrouter.ai/api/v1', 'OPENROUTER_KEY', config, messages)
        elif model_name in ["sonar", "sonar-pro", "sonar-deep-research"]:
            from .llms.LLMAPI_Endpoint_OpenAILike import LLMAPI_OpenAILike
            return LLMAPI_OpenAILike.call(model_name, 'https://api.perplexity.ai', 'PERPLEXITY_API_KEY', config, messages)
        else:
            raise ValueError("サポートされていないモデル名です")

    def tool_call(self, tool_name: str, args: dict) -> dict:
        if tool_name in ['echo', 'moch']:
            return {"response": args['user_input']}
        else:
            raise ValueError("実装されていないツール名です")