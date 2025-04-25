from pydantic import BaseModel
from ulid import ULID
import datetime

class ChatMessageData(BaseModel):
    """
    単一メッセージの保存
    """
    message_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    role: str
    message: str
    system_name: str
    subsystem_name: str
    is_error: bool

    @classmethod
    def create(cls, role: str, message: str, system_name: str, subsystem_name: str = "(Root)"):
        return cls(
            message_id=str(ULID()),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            role=role,
            message=message,
            system_name=system_name,
            subsystem_name=subsystem_name,
            is_error=False)

    def __str__(self):
        return f"{self.system_name} ({self.subsystem_name}): {self.message} @ {self.updated_at}"

class ChatLogData(BaseModel):
    """
    複数チャットメッセージを束ねた一つのチャットログ
    """
    chat_id: str
    status: str
    system_name: str
    chat_title: str
    messages: list[ChatMessageData]

    @classmethod
    def create(cls, chat_id: str, system_name: str):
        return cls(
            chat_id=chat_id,
            status="wait",
            system_name=system_name,
            chat_title="(Untitled)",
            messages=[])

    def add_message(self, role: str, message: str, subsystem_name: str = "(Not-specified)"):
        self.messages.append(ChatMessageData.create(role=role, message=message, system_name=self.system_name, subsystem_name=subsystem_name))

    def __str__(self):
        return f"Chat ID: {self.chat_id} - Messages: {len(self.messages)}"
