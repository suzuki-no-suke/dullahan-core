from .FunctionProvider import FunctionProvider
from .chatlog.DBChatLog import DbChatLog
from .memory.DBMemory import DBMemory

class Factory_DBProvider:
    @classmethod
    def create(cls, config: dict) -> FunctionProvider:
        provider = FunctionProvider()
        provider.memory = DBMemory(config)
        provider.logs = DbChatLog(config)
        return provider

