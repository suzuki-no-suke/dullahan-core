import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dullahan.db.models import Base
from dullahan.system.chathist.DBChatHistory import DBChatHistory
from dullahan.defs.ctrldef import SingleChatHistory

# テスト用のインメモリSQLiteデータベースを作成
@pytest.fixture
def db_engine():
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
def chat_history(db_engine):
    config = {
        'db_url': 'sqlite:///:memory:'
    }
    history = DBChatHistory(config)
    history.db_conn.engine = db_engine
    return history

def test_create_chat(chat_history):
    # 新しいチャットを作成
    chat_id = chat_history.create_chat("test_system")
    
    # チャットが存在することを確認
    assert chat_history.is_exists(chat_id) is True

def test_get_chat_history(chat_history):
    # テストデータを準備
    system_name = "test_system"
    chat_id = chat_history.create_chat(system_name)
    
    # チャット履歴を取得して検証
    result = chat_history.get_chat_history(chat_id)
    assert result.chat_id == chat_id
    assert result.system_name == system_name

def test_is_exists(chat_history):
    # 存在しないチャットIDを確認
    assert chat_history.is_exists("non_existent_chat") is False
    
    # 存在するチャットIDを確認
    chat_id = chat_history.create_chat("test_system")
    assert chat_history.is_exists(chat_id) is True
