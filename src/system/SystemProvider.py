from typing import Optional
from .interface.IBotRegist import IBotRegist
from .interface.IChatHistory import IChatHistory

class SystemProvider:
    def __init__(self):
        self.history: Optional[IChatHistory] = None
        self.bot_regist: Optional[IBotRegist] = None

    def serialize(self):
        self.history.serialize()

    def deserialize(self):
        self.history.deserialize()

