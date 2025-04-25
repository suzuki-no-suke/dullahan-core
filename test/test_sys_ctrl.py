import pytest
from unittest.mock import Mock
from src.ChatSystem import ChatSystem
from src.ChatControl import ChatControl
from src.system.SystemProvider import SystemProvider
from src.provider.FunctionProvider import FunctionProvider

def test_chat_system_initialization():
    # モックの作成
    system_provider = Mock(spec=SystemProvider)
    function_provider = Mock(spec=FunctionProvider)
    
    # ChatSystemの初期化テスト
    chat_system = ChatSystem(system_provider, function_provider)
    
    # 初期化されたオブジェクトが正しい型であることを確認
    assert isinstance(chat_system, ChatSystem)
    
    # 必要な属性が存在することを確認
    assert hasattr(chat_system, 'system_provider')
    assert hasattr(chat_system, 'function_provider')
    
    # プロバイダーが正しく設定されていることを確認
    assert chat_system.system_provider == system_provider
    assert chat_system.function_provider == function_provider

def test_generate_ctrl():
    # モックの作成
    system_provider = Mock(spec=SystemProvider)
    function_provider = Mock(spec=FunctionProvider)
    
    # ChatSystemの初期化
    chat_system = ChatSystem(system_provider, function_provider)
    
    # generate_ctrlメソッドのテスト
    chat_control = chat_system.generate_ctrl()
    
    # 生成されたオブジェクトが正しい型であることを確認
    assert isinstance(chat_control, ChatControl)
    
    # プロバイダーが正しく設定されていることを確認
    assert chat_control.system_provider == system_provider
    assert chat_control.provider == function_provider
