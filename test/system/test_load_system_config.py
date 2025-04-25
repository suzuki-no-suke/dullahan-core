import pytest
import os
import tempfile
from src.dullahan.system.LoadSystemConfig import LoadSystemConfig

def test_load_system_config_success():
    # 一時的なXMLファイルを作成
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp:
        tmp.write('''<?xml version="1.0" encoding="UTF-8"?>
<root>
    <configuration>
        <key1>value1</key1>
        <key2>value2</key2>
    </configuration>
</root>''')
        tmp_path = tmp.name

    try:
        # 設定を読み込む
        config = LoadSystemConfig.load(tmp_path)
        
        # 結果の検証
        assert config['key1'] == 'value1'
        assert config['key2'] == 'value2'
    finally:
        # 一時ファイルの削除
        os.unlink(tmp_path)

def test_load_system_config_file_not_found():
    # 存在しないファイルパスを指定
    with pytest.raises(FileNotFoundError) as exc_info:
        LoadSystemConfig.load('non_existent_file.xml')
    
    assert 'Config file not found' in str(exc_info.value)

def test_load_system_config_empty_configuration():
    # 空のconfigurationを持つXMLファイルを作成
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp:
        tmp.write('''<?xml version="1.0" encoding="UTF-8"?>
<root>
    <configuration>
    </configuration>
</root>''')
        tmp_path = tmp.name

    try:
        # 設定を読み込む
        config = LoadSystemConfig.load(tmp_path)
        
        # 結果の検証
        assert config == {}
    finally:
        # 一時ファイルの削除
        os.unlink(tmp_path)
