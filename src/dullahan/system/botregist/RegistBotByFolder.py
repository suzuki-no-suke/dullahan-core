from ..interface.IBotRegist import IBotRegist
from ..LoadBotConfig import LoadBotConfig
import os
import glob
from typing import Dict, Any

class RegistBotByFolder(IBotRegist):
    def __init__(self, system_config: str):
        super().__init__(system_config)
        self.system_config = system_config
        self.bot_configs: Dict[str, Dict[str, Any]] = {}
        self.bot_folder = self.system_config['bot_configuration_dir_path']
        self._load_all()

    def load(self, system_name: str) -> dict:
        """指定されたボット名の設定を取得する

        Args:
            system_name (str): ボット名

        Returns:
            dict: ボットの設定情報

        Raises:
            KeyError: 指定されたボット名が見つからない場合
        """
        if system_name not in self.bot_configs:
            raise KeyError(f"指定されたボット名が見つかりません: {system_name}")
        return self.bot_configs[system_name]

    def _load_all(self):
        """指定されたフォルダ内の全てのXMLファイルを読み込む"""
        if not os.path.exists(self.bot_folder):
            raise FileNotFoundError(f"指定されたフォルダが見つかりません: {self.bot_folder}")

        # XMLファイルを列挙
        xml_files = glob.glob(os.path.join(self.bot_folder, "*.xml"))
        
        for xml_file in xml_files:
            try:
                # 設定を読み込む
                config = LoadBotConfig.load_bot_config(xml_file)
                
                # system_nameをキーとして設定を保存
                if 'profile' in config and 'system_name' in config['profile']:
                    system_name = config['profile']['system_name']
                    self.bot_configs[system_name] = config
            except Exception as e:
                print(f"警告: {xml_file} の読み込みに失敗しました: {str(e)}")

    def list_bot_names(self) -> list[str]:
        """
        ボット名を全て返す

        Returns:
            list[str]: 利用可能なボット名のリスト
        """
        return list(self.bot_configs.keys())

    def get_config(self, system_name: str) -> dict:
        """指定されたボット名の設定を取得する

        Args:
            system_name (str): ボット名

        Returns:
            dict: ボットの設定情報

        Raises:
            KeyError: 指定されたボット名が見つからない場合
        """
        return self.load(system_name)

    def is_exist(self, system_name: str):
        return system_name in self.bot_configs