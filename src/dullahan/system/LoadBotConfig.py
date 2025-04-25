
import xml.etree.ElementTree as ET
from typing import Dict, Any
import os

class LoadBotConfig:
    @classmethod
    def load_bot_config(cls, config_path: str) -> Dict[str, Any]:
        """
        XML設定ファイルを読み込み、辞書形式で返す
        
        Args:
            config_path (str): 設定ファイルのパス
            
        Returns:
            Dict[str, Any]: 設定内容を格納した辞書
            
        Raises:
            NotImplementedError: XML以外のファイル形式が指定された場合
            FileNotFoundError: 指定されたファイルが存在しない場合
        """
        # ファイルが存在するか確認
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"指定されたファイルが見つかりません: {config_path}")

        # ファイルの拡張子を確認
        _, ext = os.path.splitext(config_path)
        if ext.lower() == '.xml':
            # XMLファイルの読み込み
            tree = ET.parse(config_path)
            root = tree.getroot()
            
            config_dict = {}
            
            # profileの処理
            profile = root.find('profile')
            if profile is not None:
                config_dict['profile'] = {
                    child.tag: child.text.strip() if child.text else ''
                    for child in profile
                }
            
            # configurationの処理
            config = root.find('configuration')
            if config is not None:
                config_dict['configuration'] = {}
                for child in config:
                    if child.tag == 'temperature':
                        config_dict['configuration'][child.tag] = float(child.text)
                    else:   # other texts
                        config_dict['configuration'][child.tag] = child.text.strip() if child.text else ''
            
            # initial_stateの処理
            initial_state = root.find('initial_state')
            if initial_state is not None:
                config_dict['initial_state'] = {}
                for child in initial_state:
                    var_type = child.get('type', 'text')
                    value = child.text.strip() if child.text else ''
                    if var_type == 'integer':
                        value = int(value)
                    elif var_type == 'float':
                        value = float(value)
                    config_dict['initial_state'][child.get('name')] = value
            
            # promptsの処理
            prompts = root.find('prompts')
            if prompts is not None:
                config_dict['prompts'] = {
                    prompt.get('name'): prompt.text.strip() if prompt.text else ''
                    for prompt in prompts.findall('defprompt')
                }
            
            return config_dict
        elif ext.lower() == '.yaml':
            raise NotImplementedError(f"Yamlファイルは現在対応していません。指定されたファイル: {config_path}")
        else:
            raise NotImplementedError(f"非対応の型式です。指定されたファイル: {config_path}")
