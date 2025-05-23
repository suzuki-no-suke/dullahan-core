from src.dullahan.provider.FunctionProvider import FunctionProvider
from src.dullahan.defs.datadef import ChatMessageData
from src.dullahan.defs.botdef import IBotBase

class SamePromptCall(IBotBase):
    def __init__(self, provider: FunctionProvider, chat_id: str, config: dict):
        self.config_check(config)
        super().__init__(provider, chat_id, config)

    def config_check(self, config: dict):
        super().config_check(config)
        if 'guidance' not in config['prompts']:
            raise ValueError(".//prompts/guidance is mandatory")
        if 'system' not in config['prompts']:
            raise ValueError(".//prompts/system is mandatory")
        if 'prompt' not in config['prompts']:
            raise ValueError(".//prompts/prompt is mandatory")
        if 'chatmodel' not in config['configuration']:
            raise ValueError(".//configuration/chatmodel is mandatory")

    def opening(self):
        self.provider.logs.add_log(self.chat_id, [
            ChatMessageData.create("guidance", self.config['prompts']['guidance'], self.system_name),
            ChatMessageData.create("system", self.config['prompts']['system'], self.system_name)
        ])

    def chat(self, user_input: str):
        model_name = self.config['configuration']['chatmodel']
        llm_config = {}
        prompt = self.helper.render_template(self.config['prompts']['prompt'], {'user_input': user_input})
        self.provider.logs.add_log(self.chat_id, [
            ChatMessageData.create("user", prompt, self.system_name)
        ])
        response = self.helper.llm_call(model_name, llm_config, self.provider.logs.get_log(self.chat_id).messages)
        self.provider.logs.add_log(self.chat_id, [
            ChatMessageData.create("assistant", response, self.system_name, model_name),
        ])
