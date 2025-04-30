import pytest
from unittest.mock import Mock
from src.dullahan.defs.botdef import IBotBase
from src.dullahan.provider.FunctionProvider import FunctionProvider

class MochBot(IBotBase):
    def __init__(self, provider, chat_id, config):
        super().__init__(provider, chat_id, config)
        self._opening_message = "Test opening message"
        self._chat_response = "Test response to: {user_input}"

    def opening(self):
        return self._opening_message
    
    def chat(self, user_input: str, subsystem_name: str):
        self.provider.chat(user_input, subsystem_name)
        return self._chat_response.format(user_input=user_input)

@pytest.fixture
def mock_provider():
    provider = Mock(spec=FunctionProvider)
    provider.chat = Mock(return_value="Test response")
    return provider

@pytest.fixture
def chat_id():
    return "test_chat_id"

@pytest.fixture
def valid_config():
    return {
        'profile': {
            'system_name': 'test_bot'
        }
    }

@pytest.fixture
def bot(mock_provider, chat_id, valid_config):
    return MochBot(mock_provider, chat_id, valid_config)

def test_initialization(bot, mock_provider, chat_id, valid_config):
    """初期化のテスト"""
    assert bot.system_name == 'test_bot'
    assert bot.chat_id == chat_id
    assert bot.config == valid_config
    assert bot.provider == mock_provider

@pytest.mark.parametrize("invalid_config", [
    {},  # profileなし
    {'profile': {}},  # system_nameなし
])
def test_invalid_config(mock_provider, chat_id, invalid_config):
    """無効な設定のテスト"""
    with pytest.raises(ValueError):
        IBotBase(mock_provider, chat_id, invalid_config)

def test_opening(bot):
    """openingメソッドのテスト"""
    result = bot.opening()
    assert result == "Test opening message"

def test_chat(bot):
    """chatメソッドのテスト"""
    test_input = "Hello"
    subsystem_name = "test_subsystem"
    result = bot.chat(test_input, subsystem_name)
    assert result == f"Test response to: {test_input}"
    bot.provider.chat.assert_called_with(test_input, subsystem_name)
