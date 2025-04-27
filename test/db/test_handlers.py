import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dullahan.db.handlers import ChatHandler, ChatMemoryHandler
from dullahan.db.models import Base

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_chat_handler_create(db_session):
    handler = ChatHandler(db_session)
    chat_log_id = handler.create("test_system")
    assert chat_log_id is not None

def test_chat_handler_update_title(db_session):
    handler = ChatHandler(db_session)
    chat_log_id = handler.create("test_system")
    handler.update_title(chat_log_id, "テストタイトル")
    # タイトルの更新を確認するための追加の検証が必要です

def test_chat_handler_add_message(db_session):
    handler = ChatHandler(db_session)
    chat_log_id = handler.create("test_system")
    message_id = handler.add_message(
        chat_log_id,
        "user",
        "テストメッセージ",
        "test_system",
        "test_subsystem"
    )
    assert message_id is not None

def test_chat_handler_get_single_message(db_session):
    handler = ChatHandler(db_session)
    chat_log_id = handler.create("test_system")
    message_id = handler.add_message(
        chat_log_id,
        "user",
        "テストメッセージ",
        "test_system",
        "test_subsystem"
    )
    message = handler.get_single_message(message_id)
    assert message is not None
    assert message.message == "テストメッセージ"

def test_chat_handler_get_whole_log(db_session):
    handler = ChatHandler(db_session)
    chat_log_id = handler.create("test_system")
    handler.add_message(chat_log_id, "user", "メッセージ1", "test_system", "test_subsystem")
    handler.add_message(chat_log_id, "assitant", "メッセージ2", "test_system", "test_subsystem")
    messages = handler.get_whole_log(chat_log_id)
    assert len(messages) == 2

def test_chat_memory_create(db_session):
    memory_handler = ChatMemoryHandler(db_session)
    chat_log_id = "test_chat_log_id"
    memory = {"key": "value"}
    memory_id = memory_handler.create(chat_log_id, memory)
    assert memory_id is not None

def test_chat_memory_get_by_chat_log_id(db_session):
    memory_handler = ChatMemoryHandler(db_session)
    chat_log_id = "test_chat_log_id"
    memory = {"key": "value"}
    memory_handler.create(chat_log_id, memory)
    retrieved_memory = memory_handler.get_by_chat_log_id(chat_log_id)
    assert retrieved_memory is not None
    assert retrieved_memory.memory == memory

def test_chat_memory_update(db_session):
    memory_handler = ChatMemoryHandler(db_session)
    chat_log_id = "test_chat_log_id"
    initial_memory = {"key": "value"}
    memory_handler.create(chat_log_id, initial_memory)
    updated_memory = {"key": "new_value"}
    memory_handler.update(chat_log_id, updated_memory)
    retrieved_memory = memory_handler.get_by_chat_log_id(chat_log_id)
    assert retrieved_memory.memory == updated_memory

def test_chat_memory_delete(db_session):
    memory_handler = ChatMemoryHandler(db_session)
    chat_log_id = "test_chat_log_id"
    memory = {"key": "value"}
    memory_handler.create(chat_log_id, memory)
    memory_handler.delete(chat_log_id)
    retrieved_memory = memory_handler.get_by_chat_log_id(chat_log_id)
    assert retrieved_memory is None
