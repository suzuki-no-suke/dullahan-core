from typing import List, Dict, Any
import json
from pathlib import Path

from ...defs.datadef import ChatMessageData, ChatLogData
from ..interface.IChatLog import IChatLog

from ...db.connect import DBConnection
from ...db.handlers import ChatHandler
from ...db.models import ChatLog, ChatMessage

class DbChatLog(IChatLog):
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        チャットログの初期化
        Args:
            config: 設定情報（file_path: ファイルパス）
        """
        self.db_url = config['db_url']
        self.db_conn = DBConnection(self.db_url)

    def get_log(self, chat_id: str) -> ChatLogData:
        """
        指定されたチャットIDのログを取得
        Args:
            chat_id: チャットID
        Returns:
            チャットログデータ
        """
        with self.db_conn.get_new_session() as sess:
            handler = ChatHandler(sess)
            messages = handler.get_whole_log(chat_id)
            
            if not messages:
                raise ValueError(f"Chat log MUST get after create. : {chat_id}")
            
            chat_log = ChatLogData.create(chat_id, messages[0].system_name)
            for msg in messages:
                chat_log.messages.append(ChatMessageData(
                    message_id=msg.id,
                    created_at=msg.created_at,
                    updated_at=msg.updated_at,
                    role=msg.role,
                    message=msg.message,
                    system_name=msg.system_name,
                    subsystem_name=msg.subsystem_name,
                    is_error=msg.is_error
                ))
            return chat_log

    def add_log(self, chat_id: str, messages: List[ChatMessageData]) -> None:
        """
        チャットログを追加
        Args:
            chat_id: チャットID
            messages: 追加するメッセージのリスト
        """
        if not messages or len(messages) <= 0:
            return

        with self.db_conn.get_new_session() as sess:
            handler = ChatHandler(sess)
            
            # チャットログは作成していること
            if not handler.is_exist(chat_id):
                raise ValueError(f"Chat log MUST get after create. : {chat_id}")
            
            # メッセージを追加
            for msg in messages:
                handler.add_message(chat_id, msg.role, msg.message, msg.system_name, msg.subsystem_name)

    def serialize(self):
        """
        チャットログをシリアライズしてファイルに保存
        """
        pass

    def deserialize(self):
        """
        ファイルからチャットログをデシリアライズして復元
        """
        pass
