import pytest
from src.dullahan.defs.ctrldef import SingleChatHistory, WholeChatHistory

def test_single_chat_history():
    # 正常なケース
    chat = SingleChatHistory(chat_id="123", system_name="test_system")
    assert chat.chat_id == "123"
    assert chat.system_name == "test_system"

    # 空の値でも動作するか
    chat = SingleChatHistory(chat_id="", system_name="")
    assert chat.chat_id == ""
    assert chat.system_name == ""

def test_whole_chat_history():
    # 正常なケース
    chat1 = SingleChatHistory(chat_id="123", system_name="system1")
    chat2 = SingleChatHistory(chat_id="456", system_name="system2")
    
    history = WholeChatHistory(datas={
        "key1": chat1,
        "key2": chat2
    })
    
    assert len(history.datas) == 2
    assert history.datas["key1"].chat_id == "123"
    assert history.datas["key1"].system_name == "system1"
    assert history.datas["key2"].chat_id == "456"
    assert history.datas["key2"].system_name == "system2"

    # 空のデータでも動作するか
    empty_history = WholeChatHistory(datas={})
    assert len(empty_history.datas) == 0
