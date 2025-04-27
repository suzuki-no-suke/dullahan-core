import pytest
import os
import shutil
from src.dullahan.system.Factory_SystemDBProvider import Factory_SystemDBProvider
from src.dullahan.system.SystemProvider import SystemProvider
from src.dullahan.system.chathist.DBChatHistory import DBChatHistory
from src.dullahan.system.botregist.RegistBotByFolder import RegistBotByFolder

@pytest.fixture
def sys_conf(tmp_path):
    # テスト用のディレクトリを作成
    test_bots_path = tmp_path /  "test_bots"
    
    # ディレクトリが存在しない場合は作成
    os.makedirs(test_bots_path, exist_ok=True)
    
    yield {
        "db_url": "sqlite:///:memory:",
        "bot_configuration_dir_path": test_bots_path
    }
    
    # テスト後にディレクトリを削除
    shutil.rmtree(test_bots_path, ignore_errors=True)

def test_create_system_provider(sys_conf):
    
    # プロバイダーの作成
    provider = Factory_SystemDBProvider.create(sys_conf)
    
    # 型の確認
    assert isinstance(provider, SystemProvider)
    assert isinstance(provider.history, DBChatHistory)
    assert isinstance(provider.bot_regist, RegistBotByFolder)
    
    # 設定値の確認
    assert provider.history.db_url == sys_conf["db_url"]
    assert provider.bot_regist.bot_folder == sys_conf["bot_configuration_dir_path"]
