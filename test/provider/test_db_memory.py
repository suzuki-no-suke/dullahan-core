import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from src.dullahan.provider.memory.DBMemory import DBMemory
from src.dullahan.db.models import Base, ChatLog, ChatMemory
from src.dullahan.db.handlers import ChatMemoryHandler

@pytest.fixture
def db_engine():
    # テスト用のデータベースURLを設定
    os.environ["DB_CONN"] = "sqlite:///:memory:"
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def db_memory(db_engine):
    config = {
        'db_url': 'sqlite:///:memory:'
    }
    memory = DBMemory(config)
    memory.db_conn.engine = db_engine
    return memory

def test_initialization(db_memory):
    """初期化のテスト"""
    assert db_memory.db_url == 'sqlite:///:memory:'
    assert db_memory.db_conn is not None

def test_load_nonexistent_memory(db_memory):
    """存在しないメモリの読み込みテスト"""
    chat_id = "nonexistent_chat"
    memory = db_memory.load(chat_id)
    assert memory == {}

def test_save_and_load_memory(db_memory):
    """メモリの保存と読み込みのテスト"""
    chat_id = "test_chat"
    test_memory = {"key": "value", "number": 123}
    
    # メモリを保存
    db_memory.save(chat_id, test_memory)
    
    # メモリを読み込み
    loaded_memory = db_memory.load(chat_id)
    
    assert loaded_memory == test_memory

def test_update_memory(db_memory):
    """メモリの更新テスト"""
    chat_id = "test_chat"
    initial_memory = {"key": "value"}
    updated_memory = {"key": "new_value", "new_key": "new_value"}
    
    # 初期メモリを保存
    db_memory.save(chat_id, initial_memory)
    
    # メモリを更新
    db_memory.save(chat_id, updated_memory)
    
    # 更新されたメモリを読み込み
    loaded_memory = db_memory.load(chat_id)
    
    assert loaded_memory == updated_memory

def test_delete_memory(db_memory):
    """メモリの削除テスト"""
    chat_id = "test_chat"
    test_memory = {"key": "value"}
    
    # メモリを保存
    db_memory.save(chat_id, test_memory)
    
    # メモリが存在することを確認
    assert db_memory.load(chat_id) == test_memory
    
    # メモリを削除
    db_memory.delete(chat_id)
    
    # メモリが削除されたことを確認
    assert db_memory.load(chat_id) == {}
