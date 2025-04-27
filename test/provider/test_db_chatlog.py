import pytest
from typing import List
from ulid import ULID
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from src.dullahan.provider.chatlog.DBChatLog import DbChatLog
from src.dullahan.defs.datadef import ChatMessageData, ChatLogData
from src.dullahan.db.models import ChatLog, ChatMessage, ChatLogEntry, Base
from src.dullahan.db.handlers import ChatHandler

@pytest.fixture
def db_engine():
    # テスト用のデータベースURLを設定
    os.environ["DB_CONN"] = "sqlite:///:memory:"
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def db_chatlog(db_engine):
    config = {
        'db_url': 'sqlite:///:memory:'
    }
    chat_log = DbChatLog(config)
    chat_log.db_conn.engine = db_engine
    return chat_log

def test_get_log_success(db_chatlog, db_session):
    # テストデータの準備
    chat_id = str(ULID())
    system_name = "test_system"
    
    # チャットログを作成
    chat_log = ChatLog(id=chat_id, system_name=system_name)
    db_session.add(chat_log)
    
    # メッセージを追加
    msg1_id = str(ULID())
    msg2_id = str(ULID())
    messages = [
        ChatMessage(
            id=msg1_id,
            message="Hello",
            role="user",
            system_name=system_name,
            subsystem_name="test_subsystem",
            is_error=False
        ),
        ChatMessage(
            id=msg2_id,
            message="Hi there!",
            role="assistant",
            system_name=system_name,
            subsystem_name="test_subsystem",
            is_error=False
        )
    ]
    db_session.add_all(messages)

    entries = [
        ChatLogEntry(
            chat_log_id=chat_id,
            chat_message_id=msg1_id,
        ),
        ChatLogEntry(
            chat_log_id=chat_id,
            chat_message_id=msg2_id,
        ),
    ]
    db_session.add_all(entries)

    db_session.commit()
    
    # テスト実行
    result = db_chatlog.get_log(chat_id)
    
    # 結果の検証
    assert result.chat_id == chat_id
    assert result.system_name == system_name
    assert len(result.messages) == 2
    assert result.messages[0].role == "user"
    assert result.messages[0].message == "Hello"
    assert result.messages[1].role == "assistant"
    assert result.messages[1].message == "Hi there!"

def test_get_log_not_found(db_chatlog):
    # テストデータの準備
    chat_id = "non_existent_chat"
    
    # テスト実行と例外の検証
    with pytest.raises(ValueError) as exc_info:
        db_chatlog.get_log(chat_id)
    assert str(exc_info.value) == f"Chat log MUST get after create. : {chat_id}"

def test_add_log_success(db_chatlog, db_session):
    # テストデータの準備
    chat_id = "test_chat_id"
    system_name = "test_system"
    
    # チャットログを作成
    chat_log = ChatLog(id=chat_id, system_name=system_name)
    db_session.add(chat_log)
    db_session.commit()

    # 追加するメッセージ
    now = datetime.now()
    messages = [
        ChatMessageData(
            message_id=str(ULID()),
            message="New message",
            role="user",
            system_name=system_name,
            subsystem_name="test_subsystem",
            created_at=now,
            updated_at=now,
            is_error=False
        )
    ]
    
    # テスト実行
    db_chatlog.add_log(chat_id, messages)
    
    # 結果の検証
    handler = ChatHandler(db_session)
    saved_messages = handler.get_whole_log(chat_id)
    assert len(saved_messages) == 1
    assert saved_messages[0].message == "New message"
    assert saved_messages[0].role == "user"

def test_add_log_empty_messages(db_chatlog, db_session):
    # テストデータの準備
    chat_id = "test_chat_id"
    system_name = "test_system"
    
    # チャットログを作成
    chat_log = ChatLog(id=chat_id, system_name=system_name)
    db_session.add(chat_log)
    db_session.commit()
    
    # 空のメッセージリストでテスト実行
    messages = []
    db_chatlog.add_log(chat_id, messages)
    
    # 結果の検証
    handler = ChatHandler(db_session)
    saved_messages = handler.get_whole_log(chat_id)
    assert len(saved_messages) == 0

def test_add_log_not_found(db_chatlog):
    # テストデータの準備
    chat_id = "non_existent_chat"
    now = datetime.now()
    messages = [
        ChatMessageData(
            message_id=str(ULID()),
            message="New message",
            role="user",
            system_name="test_system",
            subsystem_name="test_subsystem",
            created_at=now,
            updated_at=now,
            is_error=False
        )
    ]
    
    # テスト実行と例外の検証
    with pytest.raises(ValueError) as exc_info:
        db_chatlog.add_log(chat_id, messages)
    assert str(exc_info.value) == f"Chat log MUST get after create. : {chat_id}"
