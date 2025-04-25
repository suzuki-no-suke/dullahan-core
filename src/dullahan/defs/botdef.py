from ..provider.FunctionProvider import FunctionProvider
from ..BotHelper import BotHelper

class IBotBase:
    def __init__(self, provider: FunctionProvider, chat_id: str, config: dict):
        self.config_check(config)
        self.system_name = config['profile']['system_name']
        self.chat_id = chat_id
        self.config = config
        self.provider = provider
        self.helper = BotHelper()

    def config_check(self, config: dict):
        if 'profile' not in config:
            raise ValueError("設定に 'profile' セクションがありません")
        if 'system_name' not in config['profile']:
            raise ValueError("profile セクションに 'system_name' が設定されていません")

    def opening(self):
        raise NotImplementedError("need to impe method")

    def chat(self, user_input: str):
        raise NotImplementedError("need to impe method")
