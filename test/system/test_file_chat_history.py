import pytest
import json
import os
from src.dullahan.system.chathist.FileChatHistory import FileChatHistory, SingleChatHistory, WholeChatHistory

@pytest.fixture
def history_path(tmp_path):
    return str(tmp_path / "test_history.json")

@pytest.fixture
def config(history_path):
    return {"history_path": history_path}

@pytest.fixture
def chat_history(config):
    return FileChatHistory(config)

def test_chat_history_initialization(chat_history):
    """チャット履歴の初期化テスト"""
    assert isinstance(chat_history.chats, WholeChatHistory)
    assert len(chat_history.chats.datas) == 0

def test_set_and_get_chat_history(chat_history):
    """チャット設定の設定と取得テスト"""
    chat_id = "test_chat"
    chat_data = SingleChatHistory(chat_id=chat_id, system_name="test_system")
    
    chat_history.create_chat(chat_id, chat_data)
    retrieved_data = chat_history.get_chat_history(chat_id)
    
    assert retrieved_data == chat_data
    assert retrieved_data.chat_id == chat_id
    assert retrieved_data.system_name == "test_system"

def test_serialize_and_deserialize(chat_history, history_path):
    """シリアライズとデシリアライズのテスト"""
    # テストデータを設定
    chat_id = "test_chat"
    chat_data = SingleChatHistory(chat_id=chat_id, system_name="test_system")
    chat_history.create_chat(chat_id, chat_data)
    
    # シリアライズを実行
    chat_history.serialize()
    
    # ファイルが作成されたことを確認
    assert os.path.exists(history_path)
    
    # デシリアライズを実行
    new_chat_history = FileChatHistory({"history_path": history_path})
    new_chat_history.deserialize()
    
    # データが正しく復元されたことを確認
    retrieved_data = new_chat_history.get_chat_history(chat_id)
    assert retrieved_data.chat_id == chat_id
    assert retrieved_data.system_name == "test_system"

def test_serialize_error_handling(chat_history):
    """シリアライズ時のエラーハンドリングテスト"""
    # 無効なパスを設定
    chat_history.history_path = r"INVALID:\invalid\path\test_history.json"
    
    with pytest.raises(ValueError):
        chat_history.serialize()

