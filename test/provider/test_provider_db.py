import pytest
from src.dullahan.provider.Factory_DBProvider import Factory_DBProvider
from src.dullahan.provider.memory.DBMemory import DBMemory
from src.dullahan.provider.chatlog.DBChatLog import DbChatLog

def test_create_provider():
    # テスト用の設定
    config = {
        "db_url" : "sqlite:///test.db",
    }
    
    # プロバイダーの作成
    provider = Factory_DBProvider.create(config)
    
    # プロバイダーが正しく作成されたことを確認
    assert provider is not None
    assert isinstance(provider.memory, DBMemory)
    assert isinstance(provider.logs, DbChatLog)
    
    # 設定が正しく渡されていることを確認
    assert provider.memory.db_url == config["db_url"]
    assert provider.logs.db_url == config["db_url"]
