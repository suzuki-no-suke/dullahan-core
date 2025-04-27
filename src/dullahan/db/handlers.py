from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import (
    ChatMessage, ChatLog, ChatLogEntry,
    ChatMemory
)
from typing import Optional, List

class ChatHandler:
    def __init__(self, session: Session):
        self.session = session

    def create(self, system_name: str) -> str:
        """新しいチャットログを作成する"""
        chat_log = ChatLog(
            status="wait",
            system_name=system_name
        )
        self.session.add(chat_log)
        self.session.commit()
        return chat_log.id


    def update_title(self, chat_log_id: str, title: str) -> None:
        """チャットログのタイトルを更新する"""
        stmt = select(ChatLog).where(ChatLog.id == chat_log_id)
        chat_log = self.session.execute(stmt).scalar_one_or_none()
        if chat_log:
            chat_log.chat_title = title
            self.session.commit()

    def add_message(self, chat_log_id: str, message: str, system_name: str, subsystem_name: str, is_error: bool = False) -> str:
        """チャットログにメッセージを追加する"""
        chat_message = ChatMessage(
            message=message,
            system_name=system_name,
            subsystem_name=subsystem_name,
            is_error=is_error
        )
        self.session.add(chat_message)
        self.session.flush()

        chat_log_entry = ChatLogEntry(
            chat_log_id=chat_log_id,
            chat_message_id=chat_message.id
        )
        self.session.add(chat_log_entry)
        self.session.commit()
        return chat_message.id

    def get_single_message(self, message_id: str) -> Optional[ChatMessage]:
        """単一のメッセージを取得する"""
        stmt = select(ChatMessage).where(ChatMessage.id == message_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_whole_log(self, chat_log_id: str) -> List[ChatMessage]:
        """チャットログの全メッセージを取得する"""
        stmt = (
            select(ChatMessage)
            .join(ChatLogEntry, ChatMessage.id == ChatLogEntry.chat_message_id)
            .where(ChatLogEntry.chat_log_id == chat_log_id)
            .order_by(ChatMessage.updated_at)
        )
        return list(self.session.execute(stmt).scalars().all())

class ChatMemoryHandler:
    def __init__(self, session: Session):
        self.session = session

    def create(self, chat_log_id: str, memory: dict) -> str:
        """新しいチャットメモリを作成する"""
        chat_memory = ChatMemory(
            chat_log_id=chat_log_id,
            memory=memory
        )
        self.session.add(chat_memory)
        self.session.commit()
        return chat_memory.id

    def get_by_chat_log_id(self, chat_log_id: str) -> Optional[ChatMemory]:
        """チャットログIDに基づいてメモリを取得する"""
        stmt = select(ChatMemory).where(ChatMemory.chat_log_id == chat_log_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def update(self, chat_log_id: str, memory: dict) -> None:
        """チャットメモリを更新する"""
        stmt = select(ChatMemory).where(ChatMemory.chat_log_id == chat_log_id)
        chat_memory = self.session.execute(stmt).scalar_one_or_none()
        if chat_memory:
            chat_memory.memory = memory
            self.session.commit()

    def delete(self, chat_log_id: str) -> None:
        """チャットメモリを削除する"""
        stmt = select(ChatMemory).where(ChatMemory.chat_log_id == chat_log_id)
        chat_memory = self.session.execute(stmt).scalar_one_or_none()
        if chat_memory:
            self.session.delete(chat_memory)
            self.session.commit()
