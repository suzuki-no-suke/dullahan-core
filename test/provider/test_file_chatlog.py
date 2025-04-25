import pytest
from typing import Dict, Any
from datetime import datetime

from src.dullahan.provider.chatlog.FileChatLog import FileChatLog
from src.dullahan.defs.datadef import ChatMessageData

@pytest.fixture
def temp_file_path(tmp_path):
    return tmp_path / "test_chat_log.json"

@pytest.fixture
def file_chat_log(temp_file_path):
    config: Dict[str, Any] = {"chatlog_file_path": str(temp_file_path)}
    return FileChatLog(config)

@pytest.fixture
def sample_messages():
    return [
        ChatMessageData.create(
            role="user",
            message="Hello",
            system_name="test_system",
            subsystem_name="test_subsystem"
        ),
        ChatMessageData.create(
            role="assistant",
            message="Hi there!",
            system_name="test_system",
            subsystem_name="test_subsystem"
        )
    ]

def test_initialization(temp_file_path):
    config: Dict[str, Any] = {"chatlog_file_path": str(temp_file_path)}
    chat_log = FileChatLog(config)
    
    assert chat_log.file_path == temp_file_path
    assert isinstance(chat_log.whole_logs.logs, dict)

def test_add_and_get_log(file_chat_log, sample_messages):
    chat_id = "test_chat"
    
    # ログを追加
    file_chat_log.add_log(chat_id, sample_messages)
    
    # ログを取得して検証
    log_data = file_chat_log.get_log(chat_id)
    assert log_data.system_name == "test_system"
    assert len(log_data.messages) == 2
    assert log_data.messages[0].message == "Hello"
    assert log_data.messages[1].message == "Hi there!"
    assert log_data.messages[0].subsystem_name == "test_subsystem"
    assert log_data.messages[1].subsystem_name == "test_subsystem"

def test_serialize_and_deserialize(file_chat_log, sample_messages, temp_file_path):
    chat_id = "test_chat"
    
    # ログを追加
    file_chat_log.add_log(chat_id, sample_messages)
    
    # シリアライズ
    file_chat_log.serialize()

    # デシリアライズして検証
    new_chat_log = FileChatLog({"chatlog_file_path": str(temp_file_path)})
    log_data = new_chat_log.get_log(chat_id)
    assert log_data.system_name == "test_system"
    assert len(log_data.messages) == 2
    assert log_data.messages[0].message == "Hello"
    assert log_data.messages[1].message == "Hi there!"
    
    # created_atの復元を確認
    assert isinstance(log_data.messages[0].created_at, datetime)
    assert isinstance(log_data.messages[1].created_at, datetime)
    assert log_data.messages[0].created_at == sample_messages[0].created_at
    assert log_data.messages[1].created_at == sample_messages[1].created_at

def test_empty_messages(file_chat_log):
    chat_id = "test_chat"
    empty_messages = []
    
    # 空のメッセージリストを追加
    file_chat_log.add_log(chat_id, empty_messages)
    
    # チャットIDが存在しないことを確認
    assert chat_id not in file_chat_log.whole_logs.logs

def test_multiple_chats(file_chat_log, sample_messages):
    chat_id1 = "chat1"
    chat_id2 = "chat2"
    
    # 複数のチャットにログを追加
    file_chat_log.add_log(chat_id1, sample_messages)
    file_chat_log.add_log(chat_id2, sample_messages)
    
    # 両方のチャットが存在することを確認
    assert chat_id1 in file_chat_log.whole_logs.logs
    assert chat_id2 in file_chat_log.whole_logs.logs
    assert len(file_chat_log.whole_logs.logs) == 2
