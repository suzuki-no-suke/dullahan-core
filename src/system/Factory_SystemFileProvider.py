from .SystemProvider import SystemProvider
from .chathist.FileChatHistory import FileChatHistory
from .botregist.RegistBotByFolder import RegistBotByFolder

class Factory_SystemFileProvider:
    @classmethod
    def create(cls, system_config: dict) -> SystemProvider:
        provider = SystemProvider()
        provider.history = FileChatHistory(system_config)
        provider.bot_regist = RegistBotByFolder(system_config)
        return provider


