from typing import Optional
from .interface.IChatLog import IChatLog
from .interface.IChatMemory import IChatMemory

class FunctionProvider:
    def __init__(self) -> None:
        self.logs: Optional[IChatLog] = None
        self.memory: Optional[IChatMemory] = None

    def serialize(self):
        self.logs.serialize()
        self.memory.serialize()

    def deserialize(self):
        self.logs.deserialize()
        self.memory.deserialize()

