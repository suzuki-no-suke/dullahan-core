from .FunctionProvider import FunctionProvider
from .chatlog.FileChatLog import FileChatLog
from .memory.FileMemory import FileMemory

class Factory_LocalFileProvider:
    @classmethod
    def create(cls, config: dict) -> FunctionProvider:
        provider = FunctionProvider()
        provider.memory = FileMemory(config)
        provider.logs = FileChatLog(config)
        return provider

