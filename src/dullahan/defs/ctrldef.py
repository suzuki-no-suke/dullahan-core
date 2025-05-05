from pydantic import BaseModel

class SingleChatHistory(BaseModel):
    chat_id: str
    system_name: str
    is_hidden: bool

class WholeChatHistory(BaseModel):
    datas: dict[str, SingleChatHistory]


