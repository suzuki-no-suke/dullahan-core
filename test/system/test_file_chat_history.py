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
    chat_id = chat_history.create_chat("test_system")
    retrieved_data = chat_history.get_chat_history(chat_id)
    
    assert retrieved_data.chat_id == chat_id
    assert retrieved_data.system_name == "test_system"

def test_serialize_and_deserialize(chat_history, history_path):
    """シリアライズとデシリアライズのテスト"""
    # テストデータを設定
    chat_id = chat_history.create_chat("test_system")
    
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

def test_list_all_chat_history(chat_history):
    """すべてのチャット履歴のリスト取得テスト"""
    # 複数のチャットを作成
    chat_ids = []
    for i in range(3):
        chat_id = chat_history.create_chat(f"test_system_{i}")
        chat_ids.append(chat_id)
    
    # すべてのチャットIDを取得して検証
    all_chat_ids = chat_history.list_all_chat_history()
    assert len(all_chat_ids) == 3
    for chat_id in chat_ids:
        assert chat_id in all_chat_ids

