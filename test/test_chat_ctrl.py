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
    provider.logs = MagicMock()
    provider.logs.get_log = MagicMock()
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
    mock_chat_history = MagicMock()
    mock_chat_history.system_name = system_name
    mock_system_provider.history.get_chat_history.return_value = mock_chat_history
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
    subsystem_name = "(Unspecified)"
    chat_control.chat(chat_id, user_input)
    mock_bot.chat.assert_called_once_with(user_input, subsystem_name)

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

def test_list_all_bot_config(chat_control, mock_system_provider):
    mock_bot_names = ["Bot1", "Bot2"]
    mock_bot_configs = [{"name": "Bot1"}, {"name": "Bot2"}]
    
    mock_system_provider.bot_regist.list_bot_names.return_value = mock_bot_names
    mock_system_provider.bot_regist.get_config.side_effect = mock_bot_configs
    
    result = chat_control.list_all_bot_config()
    
    assert result == mock_bot_configs
    mock_system_provider.bot_regist.list_bot_names.assert_called_once()
    assert mock_system_provider.bot_regist.get_config.call_count == len(mock_bot_names)

def test_list_all_logs(chat_control, mock_system_provider, mock_function_provider):
    mock_chat_ids = ["chat1", "chat2"]
    mock_logs = [MagicMock(), MagicMock()]
    
    mock_system_provider.history.list_all_chat_history.return_value = mock_chat_ids
    mock_function_provider.logs.get_log.side_effect = mock_logs
    
    result = chat_control.list_all_logs()
    
    assert result == mock_logs
    mock_system_provider.history.list_all_chat_history.assert_called_once()
    assert mock_function_provider.logs.get_log.call_count == len(mock_chat_ids)

def test_get_single_log(chat_control, mock_system_provider, mock_function_provider):
    chat_id = "test_chat_id"
    mock_log = MagicMock()
    
    mock_system_provider.history.is_exists.return_value = True
    mock_function_provider.logs.get_log.return_value = mock_log
    
    result = chat_control.get_single_log(chat_id)
    
    assert result == mock_log
    mock_system_provider.history.is_exists.assert_called_once_with(chat_id)
    mock_function_provider.logs.get_log.assert_called_once_with(chat_id)

def test_get_single_log_not_found(chat_control, mock_system_provider):
    chat_id = "non_existent_chat"
    mock_system_provider.history.is_exists.return_value = False
    
    with pytest.raises(ValueError) as exc_info:
        chat_control.get_single_log(chat_id)
    
    assert str(exc_info.value) == f"specified chat not exists : {chat_id}"
    mock_system_provider.history.is_exists.assert_called_once_with(chat_id)
