import pytest
from sqlalchemy import text
from dullahan.db.connect import DBConnection, DbSession

def test_db_connection_initialization():
    """DBConnectionの初期化テスト"""
    db_uri = "sqlite:///:memory:"
    db_conn = DBConnection(db_uri)
    
    assert db_conn.db_uri == db_uri
    assert db_conn.engine is not None

def test_db_connection_default_env(monkeypatch):
    """デフォルト環境変数からの接続テスト"""
    test_db_uri = "sqlite:///:memory:"
    monkeypatch.setenv("DB_CONN", test_db_uri)
    
    db_conn = DBConnection.default_env()
    assert db_conn.db_uri == test_db_uri
    assert db_conn.engine is not None

def test_db_session_context_manager():
    """DbSessionのコンテキストマネージャーテスト"""
    db_uri = "sqlite:///:memory:"
    db_conn = DBConnection(db_uri)
    
    with db_conn.get_new_session() as session:
        assert session.session is not None
        # 基本的なクエリが実行できることを確認
        result = session.session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    
    # コンテキストマネージャーを抜けた後、セッションが閉じられていることを確認
    assert session.session is None
