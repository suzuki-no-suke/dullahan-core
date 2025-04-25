import pytest
import os
from src.provider.Factory_LocalFileProvider import LocalFileProvider
from src.provider.FunctionProvider import FunctionProvider

@pytest.fixture
def temp_config(tmp_path):
    """テスト用の一時ディレクトリを使用した設定を作成するフィクスチャ"""
    memory_file = tmp_path / "test_memory.json"
    chatlog_file = tmp_path / "test_log.json"
    
    return {
        "memory_file_path": str(memory_file),
        "chatlog_file_path": str(chatlog_file),
    }

def test_moch_factory_creation(temp_config):
    # ファクトリを使用してFunctionProviderを作成
    provider = LocalFileProvider.create(temp_config)
    
    # 作成されたオブジェクトがFunctionProviderのインスタンスであることを確認
    assert isinstance(provider, FunctionProvider)
    
    # 各コンポーネントが正しく設定されていることを確認
    assert provider.memory is not None
    assert provider.logs is not None
    
    # config で指定したパスに設定ファイルが書き込まれているかの確認
    provider.memory.serialize()
    provider.logs.serialize()
    assert temp_config["memory_file_path"] and temp_config["chatlog_file_path"]
    assert os.path.exists(temp_config["memory_file_path"])
    assert os.path.exists(temp_config["chatlog_file_path"])

def test_moch_factory_with_invalid_config():
    # 無効な設定でテスト
    with pytest.raises(Exception):
        LocalFileProvider.create({})
        # 例外発生後にデフォルトのパスにファイルが存在しないことを確認
        default_memory_path = "./chat_memory.json"
        default_chatlog_path = "./chat_log.json"
        
        assert not os.path.exists(default_memory_path), "デフォルトのメモリファイルが存在しています"
        assert not os.path.exists(default_chatlog_path), "デフォルトのチャットログファイルが存在しています"
