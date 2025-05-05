import os
import json
from ulid import ULID
from ...defs.ctrldef import WholeChatHistory, SingleChatHistory
from ..interface.IChatHistory import IChatHistory

class FileChatHistory(IChatHistory):
    def __init__(self, config: dict):
        super().__init__(config)
        self.history_path = self.config['history_path']
        self.chats = WholeChatHistory(datas={})

    def get_chat_history(self, chat_id: str) -> SingleChatHistory:
        return self.chats.datas[chat_id]

    def create_chat(self, system_name: str) -> str:
        chat_id = str(ULID())
        self.chats.datas[chat_id] = SingleChatHistory(chat_id=chat_id, system_name=system_name)
        return chat_id

    def is_exists(self, chat_id: str) -> bool:
        return chat_id in self.chats.datas.keys() and not self.chats.datas[chat_id].is_hidden

    def list_all_chat_history(self) -> list[str]:
        return [chat_id for chat_id, d in self.chats.datas.items() if not d.is_hidden]

    def hidden_history(self, chat_id: str):
        self.chats.datas[chat_id].is_hidden = True

    def list_all_chat_history_with_hidden_history(self) -> list[str]:
        return list(self.chats.datas.keys())

    def serialize(self):
        try:
            os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
            with open(self.history_path, 'w', encoding='utf-8') as f:
                data = self.chats.model_dump_json(indent=2)
                f.write(data)
        except Exception as e:
            raise ValueError(f"チャット履歴の保存に失敗しました: {e}")

    def deserialize(self):
        if not os.path.exists(self.history_path):
            self.chats = WholeChatHistory(datas={})
            return

        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                data = f.read()
                self.chats = WholeChatHistory.model_validate_json(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"チャット履歴ファイルのJSON形式が不正です: {e}")
        except FileNotFoundError as e:
            raise ValueError(f"チャット履歴ファイルが見つかりません: {e}")

