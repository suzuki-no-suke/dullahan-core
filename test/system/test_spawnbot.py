import pytest
import sys
from unittest.mock import MagicMock, patch

from src.dullahan.system.SpawnBot import SpawnBot
from src.dullahan.defs.botdef import IBotBase
from src.dullahan.provider.FunctionProvider import FunctionProvider

# テスト用のモックモジュールとクラス
class MockBotClass(IBotBase):
    def __init__(self, provider, chat_id, config):
        self.initialized = True
        self.provider = provider
        self.chat_id = chat_id
        self.config = config

# FunctionProviderのモック
@pytest.fixture
def mock_provider():
    return MagicMock(spec=FunctionProvider)

# 基本的な読み込みテスト
def test_spawn_bot_success(mock_provider):
    # テスト用の設定
    bot_config = {
        'profile': {
            'basemodel': 'test.module.TestBot'
        }
    }
    
    # importlib.import_moduleのモック
    with patch('src.dullahan.system.SpawnBot.importlib') as mock_importlib:
        # getattr関数のモック
        mock_module = MagicMock()
        mock_module.TestBot = MockBotClass
        mock_importlib.import_module.return_value = mock_module
        
        # テスト実行
        bot = SpawnBot.spawn(bot_config, mock_provider, "test_chat_id")
        
        # アサーション
        assert isinstance(bot, MockBotClass)
        assert isinstance(bot, IBotBase)
        assert bot.provider == mock_provider
        assert bot.chat_id == "test_chat_id"
        assert bot.config == bot_config
        mock_importlib.import_module.assert_called_once_with('test.module.TestBot')

# モジュール再読み込みのテスト
def test_spawn_bot_reload(mock_provider):
    # テスト用の設定
    bot_config = {
        'profile': {
            'basemodel': 'test.module.TestBot'
        }
    }
    
    # sys.modulesにモジュールが存在する場合のテスト
    with patch('src.dullahan.system.SpawnBot.importlib') as mock_importlib:
        with patch.dict(sys.modules, {'test.module.TestBot': MagicMock()}):
            # getattr関数のモック
            mock_module = MagicMock()
            mock_module.TestBot = MockBotClass
            mock_importlib.import_module.return_value = mock_module
            
            # テスト実行
            bot = SpawnBot.spawn(bot_config, mock_provider, "test_chat_id")
            
            # アサーション
            assert isinstance(bot, MockBotClass)
            mock_importlib.reload.assert_called_once()

# ImportErrorのテスト
def test_spawn_bot_import_error(mock_provider):
    # テスト用の設定
    bot_config = {
        'profile': {
            'basemodel': 'test.module.TestBot'
        }
    }
    
    with patch('src.dullahan.system.SpawnBot.importlib') as mock_importlib:
        mock_importlib.import_module.side_effect = ImportError("Module not found")
        
        # テスト実行
        with pytest.raises(ImportError) as excinfo:
            SpawnBot.spawn(bot_config, mock_provider, "test_chat_id")
        
        # メッセージの検証
        assert "モジュールの読み込みに失敗しました" in str(excinfo.value)
        assert "test.module.TestBot" in str(excinfo.value)

# AttributeErrorのテスト
def test_spawn_bot_attribute_error(mock_provider):
    # テスト用の設定
    bot_config = {
        'profile': {
            'basemodel': 'test.module.TestBot'
        }
    }
    
    with patch('src.dullahan.system.SpawnBot.importlib') as mock_importlib:
        # モジュールはインポートできるがクラスが見つからない場合
        mock_module = MagicMock()
        del mock_module.TestBot  # TestBotクラスを持たないようにする
        mock_importlib.import_module.return_value = mock_module
        
        # テスト実行
        with pytest.raises(AttributeError) as excinfo:
            SpawnBot.spawn(bot_config, mock_provider, "test_chat_id")
        
        # メッセージの検証
        assert "TestBot クラスが見つかりません" in str(excinfo.value)
        assert "test.module.TestBot" in str(excinfo.value)