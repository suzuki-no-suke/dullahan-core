import pytest
import json
import os

from src.dullahan.provider.memory.FileMemory import FileMemory

@pytest.fixture
def memory_file(tmp_path):
    """テスト用の一時ファイルを作成するフィクスチャ"""
    return str(tmp_path / "test_memory.json")

@pytest.fixture
def file_memory(memory_file):
    """テスト用のFileMemoryインスタンスを作成するフィクスチャ"""
    config = {'memory_file_path': memory_file}
    return FileMemory(config)

def test_initialization(file_memory, memory_file):
    """初期化のテスト"""
    assert file_memory.memory_file == memory_file
    assert file_memory.memories == {}

def test_save_and_load(file_memory):
    """保存と読み込みのテスト"""
    chat_id = "test_chat"
    test_memory = {"key": "value", "number": 123}
    
    # メモリを保存
    file_memory.save(chat_id, test_memory)
    
    # メモリを読み込み
    loaded_memory = file_memory.load(chat_id)
    
    assert loaded_memory == test_memory

def test_serialize_and_deserialize(file_memory, memory_file):
    """シリアライズとデシリアライズのテスト"""
    # テストデータを準備
    test_data = {
        "chat1": {"key1": "value1"},
        "chat2": {"key2": "value2"}
    }
    file_memory.memories = test_data
    
    # シリアライズ
    file_memory.serialize()
    
    # ファイルが存在することを確認
    assert os.path.exists(memory_file)
    
    # ファイルの内容を確認
    with open(memory_file, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert saved_data == test_data
    
    # メモリをクリアしてデシリアライズ
    file_memory.memories = {}
    file_memory.deserialize()
    
    assert file_memory.memories == test_data

def test_load_nonexistent_chat(file_memory):
    """存在しないチャットIDの読み込みテスト"""
    loaded_memory = file_memory.load("nonexistent_chat")
    assert loaded_memory == {}

def test_corrupted_file_handling(file_memory, memory_file):
    """破損したファイルの処理テスト"""
    # 不正なJSONデータを書き込む
    with open(memory_file, 'w', encoding='utf-8') as f:
        f.write("invalid json")
    
    # デシリアライズを実行
    file_memory.deserialize()
    
    # 空のメモリが作成されることを確認
    assert file_memory.memories == {}

def test_delete_existing_chat(file_memory):
    """存在するチャットIDの削除テスト"""
    chat_id = "test_chat"
    test_memory = {"key": "value"}
    
    # メモリを保存
    file_memory.save(chat_id, test_memory)
    
    # メモリが存在することを確認
    assert file_memory.load(chat_id) == test_memory
    
    # メモリを削除
    file_memory.delete(chat_id)
    
    # メモリが削除されたことを確認
    assert file_memory.load(chat_id) == {}

def test_delete_nonexistent_chat(file_memory):
    """存在しないチャットIDの削除テスト"""
    # 存在しないチャットIDを削除してもエラーが発生しないことを確認
    file_memory.delete("nonexistent_chat")
    assert file_memory.load("nonexistent_chat") == {}
