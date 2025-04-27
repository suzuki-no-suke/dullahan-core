import json
import os
from typing import Dict

from ..interface.IChatMemory import IChatMemory
from ...db.connect import DBConnection
from ...db.handlers import ChatMemoryHandler

class DBMemory(IChatMemory):
    """データベースにメモリ情報を保存する実装"""
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.db_url = config['db_url']
        self.db_conn = DBConnection(self.db_url)
    
    def load(self, chat_id: str) -> Dict:
        """指定されたチャットIDの記憶を復旧します"""
        with self.db_conn.get_new_session() as sess:
            handler = ChatMemoryHandler(sess)
            chat_memory = handler.get_by_chat_log_id(chat_id)
            if chat_memory:
                return chat_memory.memory
            return {}

    def save(self, chat_id: str, memory: Dict) -> None:
        """指定されたチャットIDの記憶を更新します"""
        with self.db_conn.get_new_session() as sess:
            handler = ChatMemoryHandler(sess)
            existing_memory = handler.get_by_chat_log_id(chat_id)
            if existing_memory:
                handler.update(chat_id, memory)
            else:
                handler.create(chat_id, memory)
    
    def delete(self, chat_id: str):
        """指定されたチャットIDの記憶を消去します"""
        with self.db_conn.get_new_session() as sess:
            handler = ChatMemoryHandler(sess)
            handler.delete(chat_id)

    def serialize(self) -> None:
        """シリアライズは不要（データベースが永続化を担当）"""
        pass
    
    def deserialize(self) -> None:
        """デシリアライズは不要（データベースが永続化を担当）"""
        pass
