import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dullahan.db.models import Base, ChatMessage, ChatLog, ChatLogEntry, ChatMemory, ChatLogStatusEnum

# テスト用のデータベースエンジンを作成
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    # テーブルを作成
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_chat_message_creation(db_session):
    # ChatMessageの作成テスト
    message = ChatMessage(
        message="テストメッセージ",
        system_name="テストシステム",
        subsystem_name="テストサブシステム"
    )
    db_session.add(message)
    db_session.commit()

    assert message.id is not None
    assert message.message == "テストメッセージ"
    assert message.system_name == "テストシステム"
    assert message.subsystem_name == "テストサブシステム"
    assert message.is_error is False
    assert message.created_at is not None
    assert message.updated_at is not None

def test_chat_log_creation(db_session):
    # ChatLogの作成テスト
    chat_log = ChatLog(
        status=ChatLogStatusEnum.WAIT,
        system_name="テストシステム",
        chat_title="テストチャット"
    )
    db_session.add(chat_log)
    db_session.commit()

    assert chat_log.id is not None
    assert chat_log.created_at is not None
    assert chat_log.updated_at is not None
    assert chat_log.status == ChatLogStatusEnum.WAIT
    assert chat_log.system_name == "テストシステム"
    assert chat_log.chat_title == "テストチャット"

def test_chat_log_entry_creation(db_session):
    # ChatLogEntryの作成テスト
    message = ChatMessage(message="テストメッセージ")
    chat_log = ChatLog(status=ChatLogStatusEnum.WAIT)
    db_session.add_all([message, chat_log])
    db_session.commit()

    entry = ChatLogEntry(
        chat_log_id=chat_log.id,
        chat_message_id=message.id
    )
    db_session.add(entry)
    db_session.commit()

    assert entry.id is not None
    assert entry.chat_log_id == chat_log.id
    assert entry.chat_message_id == message.id

def test_chat_memory_creation(db_session):
    # ChatMemoryの作成テスト
    chat_log = ChatLog(status=ChatLogStatusEnum.WAIT)
    db_session.add(chat_log)
    db_session.commit()

    memory = ChatMemory(
        chat_log_id=chat_log.id,
        memory={"key": "value"}
    )
    db_session.add(memory)
    db_session.commit()

    assert memory.id is not None
    assert memory.chat_log_id == chat_log.id
    assert memory.memory == {"key": "value"}

def test_chat_log_status_validation(db_session):
    # ChatLogのステータスバリデーションテスト
    with pytest.raises(Exception):
        chat_log = ChatLog(status="invalid_status")
        db_session.add(chat_log)
        db_session.commit()
