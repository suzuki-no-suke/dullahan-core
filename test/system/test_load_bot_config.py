import pytest
import os
import tempfile
import xml.etree.ElementTree as ET

from src.system.LoadBotConfig import LoadBotConfig

@pytest.fixture
def temp_dir():
    # テスト用の一時ディレクトリを作成
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # 後片付け
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

@pytest.fixture
def valid_xml_path(temp_dir):
    # テスト用のXMLファイルを作成
    xml_path = os.path.join(temp_dir, "test_config.xml")
    
    root = ET.Element("root")
    
    # profileセクション
    profile = ET.SubElement(root, "profile")
    ET.SubElement(profile, "name").text = "Test Bot"
    ET.SubElement(profile, "version").text = "1.0"
    
    # configurationセクション
    config = ET.SubElement(root, "configuration")
    ET.SubElement(config, "temperature").text = "0.7"
    ET.SubElement(config, "model").text = "gpt-4.1"
    
    # initial_stateセクション
    initial_state = ET.SubElement(root, "initial_state")
    var1 = ET.SubElement(initial_state, "var1")
    var1.set("name", "count")
    var1.set("type", "integer")
    var1.text = "10"
    
    var2 = ET.SubElement(initial_state, "var2")
    var2.set("name", "threshold")
    var2.set("type", "float")
    var2.text = "0.5"
    
    # promptsセクション
    prompts = ET.SubElement(root, "prompts")
    prompt1 = ET.SubElement(prompts, "defprompt")
    prompt1.set("name", "greeting")
    prompt1.text = "こんにちは"
    
    prompt2 = ET.SubElement(prompts, "defprompt")
    prompt2.set("name", "farewell")
    prompt2.text = "さようなら"
    
    # XMLファイルを保存
    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    
    return xml_path

@pytest.fixture
def invalid_ext_path(temp_dir):
    path = os.path.join(temp_dir, "test_config.txt")
    with open(path, "w") as f:
        f.write("test")
    return path

@pytest.fixture
def nonexistent_path(temp_dir):
    return os.path.join(temp_dir, "nonexistent.xml")

def test_load_valid_xml(valid_xml_path):
    """有効なXMLファイルの読み込みテスト"""
    config = LoadBotConfig.load_bot_config(valid_xml_path)
    
    # profileの検証
    assert config["profile"]["name"] == "Test Bot"
    assert config["profile"]["version"] == "1.0"
    
    # configurationの検証
    assert config["configuration"]["temperature"] == 0.7
    assert config["configuration"]["model"] == "gpt-4.1"
    
    # initial_stateの検証
    assert config["initial_state"]["count"] == 10
    assert config["initial_state"]["threshold"] == 0.5
    
    # promptsの検証
    assert config["prompts"]["greeting"] == "こんにちは"
    assert config["prompts"]["farewell"] == "さようなら"

def test_file_not_found(nonexistent_path):
    """存在しないファイルのエラー処理テスト"""
    with pytest.raises(FileNotFoundError):
        LoadBotConfig.load_bot_config(nonexistent_path)

def test_invalid_file_extension(invalid_ext_path):
    """非対応のファイル形式のエラー処理テスト"""
    with pytest.raises(NotImplementedError):
        LoadBotConfig.load_bot_config(invalid_ext_path)
