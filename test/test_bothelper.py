import pytest
from src.BotHelper import BotHelper
from src.defs.datadef import ChatMessageData

def test_render_template():
    # テンプレートとパラメータのテスト
    bot_helper = BotHelper()
    template = "こんにちは、{{ name }}さん！"
    parameters = {"name": "テストユーザー"}
    expected = "こんにちは、テストユーザーさん！"
    
    result = bot_helper.render_template(template, parameters)
    assert result == expected

def test_llm_call_echo():
    # echoモデルのテスト
    bot_helper = BotHelper()
    messages = [
        ChatMessageData.create(role="user", message="こんにちは", system_name="Unittest"),
        ChatMessageData.create(role="assistant", message="こんにちは！", system_name="Unittest")
    ]
    
    result = bot_helper.llm_call("echo", {}, messages)
    assert isinstance(result, str)
    assert result == "こんにちは"

def test_llm_call_moch():
    # mochモデルのテスト
    bot_helper = BotHelper()
    messages = [
        ChatMessageData.create(role="user", message="テストメッセージ", system_name="Unittest")
    ]
    
    result = bot_helper.llm_call("moch", {}, messages)
    assert isinstance(result, str)
    assert result == "テストメッセージ"

def test_llm_call_unsupported_model():
    # サポートされていないモデルのテスト
    bot_helper = BotHelper()
    messages = [
        ChatMessageData.create(role="user", message="こんにちは", system_name="Unittest")
    ]
    
    with pytest.raises(ValueError, match="サポートされていないモデル名です"):
        bot_helper.llm_call("unknown_model", {}, messages)

def test_tool_call_echo():
    # echoツールのテスト
    bot_helper = BotHelper()
    args = {"user_input": "テストメッセージ"}
    result = bot_helper.tool_call("echo", args)
    assert isinstance(result, dict)
    assert "response" in result
    assert result["response"] == "テストメッセージ"

def test_tool_call_moch():
    # mochツールのテスト
    bot_helper = BotHelper()
    args = {"user_input": "テストメッセージ"}
    result = bot_helper.tool_call("moch", args)
    assert isinstance(result, dict)
    assert "response" in result
    assert result["response"] == "テストメッセージ"

def test_tool_call_unsupported_tool():
    # サポートされていないツールのテスト
    bot_helper = BotHelper()
    args = {"user_input": "テストメッセージ"}
    with pytest.raises(ValueError, match="実装されていないツール名です"):
        bot_helper.tool_call("unknown_tool", args)

