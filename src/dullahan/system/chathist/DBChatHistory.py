import os
import json
from ...defs.ctrldef import WholeChatHistory, SingleChatHistory

from ..interface.IChatHistory import IChatHistory
from ...db.connect import DBConnection
from ...db.handlers import ChatHandler

class DBChatHistory(IChatHistory):
    def __init__(self, config: dict):
        super().__init__(config)
        self.db_url = config['db_url']
        self.db_conn = DBConnection(self.db_url)

    def get_chat_history(self, chat_id: str) -> SingleChatHistory:
        with self.db_conn.get_new_session() as sess:
            handler = ChatHandler(sess)
            chat_data = handler.get_chat_data(chat_id)
            return SingleChatHistory(chat_id=chat_id, system_name=chat_data.system_name)

    def create_chat(self, system_name: str) -> str:
        with self.db_conn.get_new_session() as sess:
            handler = ChatHandler(sess)
            return handler.create(system_name)

    def is_exists(self, chat_id: str) -> bool:
        with self.db_conn.get_new_session() as sess:
            handler = ChatHandler(sess)
            return handler.is_exist(chat_id)

    def list_all_chat_history(self) -> list[str]:
        with self.db_conn.get_new_session() as sess:
            handler = ChatHandler(sess)
            return handler.list_visible_chat_ids()

    def hidden_history(self, chat_id: str):
        with self.db_conn.get_new_session() as sess:
            handler = ChatHandler(sess)
            handler.set_hidden(chat_id, True)

    def list_all_chat_history_with_hidden_history(self) -> list[str]:
        with self.db_conn.get_new_session() as sess:
            handler = ChatHandler(sess)
            return handler.list_all_chat_ids_with_hidden()

    def serialize(self):
        """
        データベースのチャット履歴をシリアライズします。
        データベースを使用しているため、このメソッドは何もしません。
        """
        pass

    def deserialize(self):
        """
        データベースのチャット履歴をデシリアライズします。
        データベースを使用しているため、このメソッドは何もしません。
        """
        pass

