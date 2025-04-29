from typing import Dict
from ulid import ULID

from .provider.FunctionProvider import FunctionProvider
from .system.SystemProvider import SystemProvider
from .system.SpawnBot import SpawnBot
from .defs.botdef import IBotBase
from .defs.datadef import ChatLogData

class ChatControl:
    def __init__(self, system_provider: SystemProvider, provider: FunctionProvider):
        self.system_provider = system_provider
        self.provider = provider
        self.bots: Dict[str, IBotBase] = {}
        self.system_provider.deserialize()
        self.provider.deserialize()

    def create_chat(self, system_name: str) -> str:
        chat_id = self.system_provider.history.create_chat(system_name)
        bot = SpawnBot.spawn(self.system_provider.bot_regist.get_config(system_name), self.provider, chat_id)
        self.bots[chat_id] = bot
        return chat_id

    def reopen_chat(self, chat_id: str):
        if not self.system_provider.history.is_exists(chat_id):
            raise ValueError(f"Chat ID not found.: {chat_id}")
        chat_history = self.system_provider.history.get_chat_history(chat_id)
        bot_config = self.system_provider.bot_regist.get_config(chat_history.system_name)
        self.bots[chat_id] = SpawnBot.spawn(bot_config, self.provider, chat_id)

    def opening(self, chat_id: str):
        if chat_id not in self.bots:
            raise ValueError(f"Chat ID not found. Create first.: {chat_id}")
        self.bots[chat_id].opening()
        self.system_provider.serialize()
        self.provider.serialize()

    def chat(self, chat_id: str, user_input: str):
        if chat_id not in self.bots:
            raise ValueError(f"Chat ID not found. Create or reopen first.: {chat_id}")
        self.bots[chat_id].chat(user_input)
        self.system_provider.serialize()
        self.provider.serialize()

    def close(self):
        self.system_provider.serialize()
        self.provider.serialize()

    def list_all_bot_config(self) -> list[dict]:
        bot_names = self.system_provider.bot_regist.list_bot_names()
        return [self.system_provider.bot_regist.get_config(name) for name in bot_names]
    
    def list_all_logs(self) -> list[ChatLogData]:
        chat_ids = self.system_provider.history.list_all_chat_history()
        return [self.provider.logs.get_log(chat_id) for chat_id in chat_ids]

    def get_single_log(self, chat_id: str) -> ChatLogData:
        if not self.system_provider.history.is_exists(chat_id):
            raise ValueError(f"specified chat not exists : {chat_id}")
        return self.provider.logs.get_log(chat_id)

    def chat_is_exists(self, chat_id: str) -> bool:
        return self.system_provider.history.is_exists(chat_id)