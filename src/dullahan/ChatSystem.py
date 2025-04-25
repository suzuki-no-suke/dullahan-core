import json
from .ChatControl import ChatControl
from .system.SystemProvider import SystemProvider
from .provider.FunctionProvider import FunctionProvider

class ChatSystem:
    def __init__(self, system_provider: SystemProvider, function_provider: FunctionProvider):
        self.system_provider = system_provider
        self.function_provider = function_provider

    def generate_ctrl(self) -> ChatControl:
        return ChatControl(self.system_provider, self.function_provider)
