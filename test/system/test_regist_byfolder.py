import os
import pytest
from src.dullahan.system.botregist.RegistBotByFolder import RegistBotByFolder
import tempfile
import shutil
from pathlib import Path

class TestRegistBotByFolder:
    @pytest.fixture
    def temp_dir(self):
        # 一時ディレクトリを作成
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # テスト後に一時ディレクトリを削除
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def valid_xml_content(self):
        return """<?xml version="1.0" encoding="UTF-8"?>
<bot>
    <profile>
        <system_name>test_bot</system_name>
    </profile>
    <configuration>
        <param1>value1</param1>
        <param2>value2</param2>
    </configuration>
</bot>"""

    @pytest.fixture
    def invalid_xml_content(self):
        return "invalid xml content"

    def test_load_valid_bot(self, temp_dir, valid_xml_content):
        # テスト用のXMLファイルを作成
        xml_path = os.path.join(temp_dir, "test_bot.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(valid_xml_content)

        # システム設定を作成
        system_config = {
            "bot_configuration_dir_path": temp_dir
        }

        # RegistBotByFolderを初期化
        regist = RegistBotByFolder(system_config)

        # 設定を取得
        config = regist.load("test_bot")

        # 検証
        assert config["profile"]["system_name"] == "test_bot"
        assert config["configuration"]["param1"] == "value1"
        assert config["configuration"]["param2"] == "value2"

    def test_load_nonexistent_bot(self, temp_dir, valid_xml_content):
        # テスト用のXMLファイルを作成
        xml_path = os.path.join(temp_dir, "test_bot.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(valid_xml_content)

        # システム設定を作成
        system_config = {
            "bot_configuration_dir_path": temp_dir
        }

        # RegistBotByFolderを初期化
        regist = RegistBotByFolder(system_config)

        # 存在しないボット名を指定
        with pytest.raises(KeyError):
            regist.load("nonexistent_bot")

    def test_load_from_nonexistent_directory(self):
        # 存在しないディレクトリを指定
        system_config = {
            "bot_configuration_dir_path": "nonexistent_directory"
        }

        # RegistBotByFolderを初期化（FileNotFoundErrorが発生するはず）
        with pytest.raises(FileNotFoundError):
            RegistBotByFolder(system_config)

    def test_load_invalid_xml(self, temp_dir, invalid_xml_content):
        # 不正なXMLファイルを作成
        xml_path = os.path.join(temp_dir, "invalid_bot.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(invalid_xml_content)

        # システム設定を作成
        system_config = {
            "bot_configuration_dir_path": temp_dir
        }

        # RegistBotByFolderを初期化（警告が出力されるが、エラーは発生しない）
        regist = RegistBotByFolder(system_config)

        # 不正なXMLファイルのボットは読み込まれないことを確認
        with pytest.raises(KeyError):
            regist.load("invalid_bot")

    def test_load_bot_without_configuration(self, temp_dir):
        # configurationなしのXMLファイルを作成
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<bot>
    <profile>
        <system_name>simple_bot</system_name>
    </profile>
</bot>"""
        
        xml_path = os.path.join(temp_dir, "simple_bot.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        # システム設定を作成
        system_config = {
            "bot_configuration_dir_path": temp_dir
        }

        # RegistBotByFolderを初期化
        regist = RegistBotByFolder(system_config)

        # 設定を取得
        config = regist.load("simple_bot")

        # 検証
        assert config["profile"]["system_name"] == "simple_bot"
        assert "configuration" not in config
