from src.provider.FunctionProvider import FunctionProvider
from src.defs.datadef import ChatMessageData
from src.defs.botdef import IBotBase

class SingleFunction(IBotBase):
    def __init__(self, provider: FunctionProvider, chat_id: str, config: dict):
        self.config_check(config)
        super().__init__(provider, chat_id, config)

    def config_check(self, config: dict):
        super().config_check(config)
        if 'guidance' not in config['prompts']:
            raise ValueError(".//prompts/guidance is mandatory")
        if 'toolname' not in config['configuration']:
            raise ValueError(".//configuration/toolname is mandatory")

    def opening(self):
        self.provider.logs.add_log(self.chat_id, [
            ChatMessageData.create("guidance", self.config['prompts']['guidance'], self.system_name)
        ])

    def chat(self, user_input: str):
        ret = self.helper.tool_call(self.config['configuration']['toolname'], {'user_input': user_input})
        self.provider.logs.add_log(self.chat_id, [
            ChatMessageData.create("user", user_input, self.system_name),
            ChatMessageData.create("assistant", ret["response"], self.system_name, "(Tool)"),
        ])
