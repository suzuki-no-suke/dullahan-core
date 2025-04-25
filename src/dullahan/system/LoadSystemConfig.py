
import xml.etree.ElementTree as ET
import os

class LoadSystemConfig:
    @classmethod
    def load(cls, config_path: str) -> dict:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        tree = ET.parse(config_path)

        # 設定を辞書化
        root = tree.getroot()
        
        config = {}
        # configurationタグの処理
        configuration = root.find('configuration')
        if configuration is not None:
            config = {}
            for child in configuration:
                # 子要素のテキスト内容を取得し、辞書に追加
                config[child.tag] = child.text.strip() if child.text else ''
        
        return config
