from typing import List, Dict, Any
import json
from pathlib import Path
from pydantic import BaseModel
import datetime

from ...defs.datadef import ChatMessageData, ChatLogData
from ..interface.IChatLog import IChatLog

class WholeLogMessage(BaseModel):
    """
    チャットログ全体を保存するためのPydanticモデル
    """
    logs: Dict[str, ChatLogData] = {}

class FileChatLog(IChatLog):
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        チャットログの初期化
        Args:
            config: 設定情報（file_path: ファイルパス）
        """
        self.file_path = Path(config["chatlog_file_path"] or "./chat_log.json")
        self.deserialize()

    def get_log(self, chat_id: str) -> ChatLogData:
        """
        指定されたチャットIDのログを取得
        Args:
            chat_id: チャットID
        Returns:
            チャットログデータ
        """
        return self.whole_logs.logs[chat_id]

    def add_log(self, chat_id: str, messages: List[ChatMessageData]) -> None:
        """
        チャットログを追加
        Args:
            chat_id: チャットID
            messages: 追加するメッセージのリスト
        """
        if len(messages) <= 0:
            return
        if chat_id not in self.whole_logs.logs:
            self.whole_logs.logs[chat_id] = ChatLogData.create(chat_id, messages[0].system_name)
        for msg in messages:
            self.whole_logs.logs[chat_id].messages.append(msg)
        self.whole_logs.logs[chat_id].updated_at = datetime.datetime.now()

    def serialize(self):
        """
        チャットログをシリアライズしてファイルに保存
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(self.whole_logs.model_dump_json(indent=2))

    def deserialize(self):
        """
        ファイルからチャットログをデシリアライズして復元
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = f.read()
                self.whole_logs = WholeLogMessage.model_validate_json(data)
        except (json.JSONDecodeError, FileNotFoundError):
            self.whole_logs = WholeLogMessage(logs={})
