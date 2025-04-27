import json
import os
from typing import Dict
from ..interface.IChatMemory import IChatMemory

class FileMemory(IChatMemory):
    """ファイルにJSON形式でメモリ情報を保存する実装"""
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.memory_file = config.get('memory_file_path', './chat_memory.json')
        self.memories = {}
        self.deserialize()
    
    def load(self, chat_id: str) -> Dict:
        """指定されたチャットIDの記憶を復旧します"""
        return self.memories.get(chat_id, {})
    
    def save(self, chat_id: str, memory: Dict) -> None:
        """指定されたチャットIDの記憶を更新します"""
        self.memories[chat_id] = memory
        self.serialize()
    
    def delete(self, chat_id: str):
        if chat_id in self.memories:
            del self.memories[chat_id]

    def serialize(self) -> None:
        """データ全体をJSONファイルに永続化します"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, ensure_ascii=False, indent=2)
    
    def deserialize(self) -> None:
        """JSONファイルからデータを復旧します"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memories = json.load(f)
            except json.JSONDecodeError:
                self.memories = {}
        else:
            self.memories = {}
