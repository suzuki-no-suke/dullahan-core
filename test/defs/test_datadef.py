from datetime import datetime

from src.defs.datadef import ChatMessageData, ChatLogData

def test_chat_message_data_initialization():
    """ChatMessageDataの初期化テスト"""
    message = ChatMessageData.create(
        role="user",
        message="こんにちは",
        system_name="test_system",
        subsystem_name="test_subsystem"
    )
    
    assert message.role == "user"
    assert message.message == "こんにちは"
    assert message.system_name == "test_system"
    assert message.subsystem_name == "test_subsystem"
    assert message.is_error is False
    assert isinstance(message.message_id, str)
    assert isinstance(message.created_at, datetime)
    assert isinstance(message.updated_at, datetime)

def test_chat_log_data_initialization():
    """ChatLogDataの初期化テスト"""
    chat_log = ChatLogData.create(
        chat_id="test_chat_id",
        system_name="test_system"
    )
    
    assert chat_log.system_name == "test_system"
    assert chat_log.status == "wait"
    assert chat_log.chat_title == "(Untitled)"
    assert len(chat_log.messages) == 0
    assert isinstance(chat_log.chat_id, str)

def test_chat_log_data_add_message():
    """ChatLogDataのメッセージ追加テスト"""
    chat_log = ChatLogData.create(
        chat_id="test_chat_id",
        system_name="test_system"
    )
    chat_log.add_message(
        role="user",
        message="テストメッセージ",
        subsystem_name="test_subsystem"
    )
    
    assert len(chat_log.messages) == 1
    message = chat_log.messages[0]
    assert message.role == "user"
    assert message.message == "テストメッセージ"
    assert message.system_name == "test_system"
    assert message.subsystem_name == "test_subsystem"
