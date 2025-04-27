from .SystemProvider import SystemProvider
from .chathist.DBChatHistory import DBChatHistory
from .botregist.RegistBotByFolder import RegistBotByFolder

class Factory_SystemDBProvider:
    @classmethod
    def create(cls, system_config: dict) -> SystemProvider:
        provider = SystemProvider()
        provider.history = DBChatHistory(system_config)
        provider.bot_regist = RegistBotByFolder(system_config)
        return provider


