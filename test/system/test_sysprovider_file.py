import pytest
import os
import shutil
from src.dullahan.system.Factory_SystemFileProvider import Factory_SystemFileProvider
from src.dullahan.system.SystemProvider import SystemProvider

@pytest.fixture
def test_dirs():
    # テスト用のディレクトリを作成
    test_history_path = "test_history"
    test_bots_path = "test_bots"
    
    # ディレクトリが存在しない場合は作成
    os.makedirs(test_history_path, exist_ok=True)
    os.makedirs(test_bots_path, exist_ok=True)
    
    yield {
        "history_path": test_history_path,
        "bot_configuration_dir_path": test_bots_path
    }
    
    # テスト後にディレクトリを削除
    shutil.rmtree(test_history_path, ignore_errors=True)
    shutil.rmtree(test_bots_path, ignore_errors=True)

def test_create_system_provider(test_dirs):
    # プロバイダーの作成
    provider = Factory_SystemFileProvider.create(test_dirs)
    
    # 型チェック
    assert isinstance(provider, SystemProvider)
    
    # コンポーネントの存在確認
    assert hasattr(provider, 'history')
    assert hasattr(provider, 'bot_regist')
    
    # 設定値の確認
    assert provider.history.history_path == test_dirs["history_path"]
    assert provider.bot_regist.bot_folder == test_dirs["bot_configuration_dir_path"]

def test_create_with_empty_config():
    # 空の設定でプロバイダーを作成
    # 空の設定では必要なキーがないためKeyErrorが発生することを確認
    with pytest.raises(KeyError):
        provider = Factory_SystemFileProvider.create({})
