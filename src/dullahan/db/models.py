from sqlalchemy import (
    Column, String, DateTime, Boolean, ForeignKey, LargeBinary, Text, CheckConstraint, Integer, JSON
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from ulid import ULID
import enum

Base = declarative_base()

# -----------------------
# Enumを文字列 + チェック制約で定義
# -----------------------
class ChatLogStatusEnum(str, enum.Enum):
    WAIT = "wait"
    INPROGRESS = "in_progress"

VALID_CHAT_LOG_STATUSES = ('wait', 'in_progress')


# =====================
# DB: Dullahan
# =====================

class ChatMessage(Base):
    __tablename__ = "chat_message"

    id = Column(String, primary_key=True, default=lambda: str(ULID()))  # ULID as string
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    message = Column(Text, nullable=False, default="")
    role = Column(String, nullable=False, default="note")
    system_name = Column(String, nullable=False, default="(Unknonw)")
    subsystem_name = Column(String, nullable=False, default="(Unknonw)")
    is_error = Column(Boolean, default=False)


class ChatLog(Base):
    __tablename__ = "chat_log"

    id = Column(String, primary_key=True, default=lambda: str(ULID()))  # ULID
    status = Column(String, nullable=False, default="wait")
    system_name = Column(String, nullable=False, default="(Unknown)")
    chat_title = Column(String, nullable=True, default="(Untitled)")

    __table_args__ = (
        CheckConstraint(status.in_(VALID_CHAT_LOG_STATUSES), name="valid_status_check"),
    )


class ChatLogEntry(Base):
    __tablename__ = "chat_log_entry"

    id = Column(String, primary_key=True, default=lambda: str(ULID()))
    chat_log_id = Column(String, ForeignKey("chat_log.id"), nullable=False)
    chat_message_id = Column(String, ForeignKey("chat_message.id"), nullable=False)

    chat_log = relationship("ChatLog")
    chat_message = relationship("ChatMessage")


class ChatMemory(Base):
    __tablename__ = "chat_memory"

    id = Column(String, primary_key=True, default=lambda: str(ULID()))
    chat_log_id = Column(String, ForeignKey("chat_log.id"), nullable=False)
    memory = Column(JSON, nullable=True)
