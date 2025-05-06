from pydantic import BaseModel
from ulid import ULID

class SingleChatHistory(BaseModel):
    chat_id: str
    system_name: str
    is_hidden: bool

    @classmethod
    def create(cls, system_name: str, chat_id: str = str(ULID())):
        return SingleChatHistory(
            chat_id=chat_id,
            system_name=system_name,
            is_hidden=False)

class WholeChatHistory(BaseModel):
    datas: dict[str, SingleChatHistory]


