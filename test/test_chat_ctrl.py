import pytest
import os
import xml.etree.ElementTree as ET
from unittest.mock import MagicMock, patch
from src.dullahan.ChatControl import ChatControl
from src.dullahan.provider.FunctionProvider import FunctionProvider
from src.dullahan.system.SystemProvider import SystemProvider
from src.dullahan.defs.botdef import IBotBase


@pytest.fixture
def mock_function_provider():
    provider = MagicMock(spec=FunctionProvider)
    provider.serialize = MagicMock()
    return provider

@pytest.fixture
def mock_system_provider():
    provider = MagicMock(spec=SystemProvider)
    provider.deserialize = MagicMock()
    provider.serialize = MagicMock()
    provider.history = MagicMock()
    provider.history.get_chat_history = MagicMock()
    provider.history.create_chat = MagicMock()
    provider.history.is_exists = MagicMock(return_value=True)  # デフォルトで存在するように設定
    provider.bot_regist = MagicMock()
    provider.bot_regist.get_config = MagicMock()
    # モックボットの設定を追加
    mock_bot_config = {
        'profile': {
            'system_name': 'TestBot',
            'basemodel': 'test.resource.MochBot'  # 絶対パスで指定
        }
    }
    provider.bot_regist.__getitem__.return_value = mock_bot_config
    provider.bot_regist.get_config.return_value = mock_bot_config
    return provider

@pytest.fixture
def chat_control(mock_system_provider, mock_function_provider):
    with patch('src.dullahan.ChatControl.SpawnBot') as mock_spawn_bot:
        mock_bot = MagicMock(spec=IBotBase)
        mock_spawn_bot.spawn = MagicMock(return_value=mock_bot)
        control = ChatControl(mock_system_provider, mock_function_provider)
        return control

def test_chat_control_initialization(chat_control, mock_system_provider, mock_function_provider):
    assert chat_control.system_provider == mock_system_provider
    assert chat_control.provider == mock_function_provider
    mock_system_provider.deserialize.assert_called_once()
    mock_function_provider.deserialize.assert_called_once()

def test_create_chat(chat_control, mock_system_provider):
    chat_id = chat_control.create_chat("TestBot")
    
    assert chat_id is not None
    assert chat_id in chat_control.bots
    mock_system_provider.history.create_chat.assert_called_once()
    assert isinstance(chat_control.bots[chat_id], IBotBase)

def test_reopen_chat(chat_control, mock_system_provider):
    chat_id = "test_chat_id"
    system_name = "TestBot"
    mock_system_provider.history.get_chat_history.return_value = system_name
    mock_system_provider.history.is_exists.return_value = True
    
    chat_control.reopen_chat(chat_id)
    
    assert chat_id in chat_control.bots
    mock_system_provider.bot_regist.get_config.assert_called_once_with(system_name)
    assert isinstance(chat_control.bots[chat_id], IBotBase)

def test_chat_operations(chat_control):
    chat_id = "test_chat_id"
    mock_bot = MagicMock(spec=IBotBase)
    chat_control.bots[chat_id] = mock_bot
    
    # openingのテスト
    chat_control.opening(chat_id)
    mock_bot.opening.assert_called_once()
    
    # chatのテスト
    user_input = "こんにちは"
    chat_control.chat(chat_id, user_input)
    mock_bot.chat.assert_called_once_with(user_input)

def test_close(chat_control, mock_system_provider, mock_function_provider):
    chat_control.close()
    mock_function_provider.serialize.assert_called_once()
    mock_system_provider.serialize.assert_called_once()

def test_invalid_chat_id(chat_control, mock_system_provider):
    # 存在しないチャットIDの場合
    mock_system_provider.history.is_exists.return_value = False
    
    with pytest.raises(ValueError):
        chat_control.opening("invalid_chat_id")
    
    with pytest.raises(ValueError):
        chat_control.chat("invalid_chat_id", "test message")
    
    with pytest.raises(ValueError):
        chat_control.reopen_chat("invalid_chat_id_2")
