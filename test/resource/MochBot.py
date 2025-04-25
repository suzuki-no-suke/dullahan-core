from src.dullahan.defs.botdef import IBotBase
from src.dullahan.provider.FunctionProvider import FunctionProvider

class MochBot(IBotBase):
    def __init__(self, provider: FunctionProvider, chat_id: str, config: dict):
        super().__init__(provider, chat_id, config)

    def config_check(self, config: dict):
        pass

    def opening(self):
        pass

    def chat(self, user_input: str):
        pass
