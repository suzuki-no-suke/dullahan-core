from typing import List, Dict, Any

from ...defs.datadef import ChatMessageData, ChatLogData

class IChatLog:
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        チャットログの初期化
        Args:
            config: 設定情報
        """
        raise NotImplementedError("IChatLog.__init__ must be implemented")

    def get_log(self, chat_id: str) -> ChatLogData:
        """
        指定されたチャットIDのログを取得
        Args:
            chat_id: チャットID
        Returns:
            チャットメッセージのリスト
        """
        raise NotImplementedError("IChatLog.get_log must be implemented")

    def add_log(self, chat_id: str, messages: List[ChatMessageData]) -> None:
        """
        チャットログを追加
        Args:
            chat_id: チャットID
            messages: 追加するメッセージのリスト
        """
        raise NotImplementedError("IChatLog.add_log must be implemented")

    def serialize(self) -> Dict[str, Any]:
        """
        チャットログをシリアライズ
        Returns:
            シリアライズされたデータ
        """
        raise NotImplementedError("IChatLog.serialize must be implemented")

    def deserialize(self, data: Dict[str, Any]) -> None:
        """
        シリアライズされたデータからチャットログを復元
        Args:
            data: シリアライズされたデータ
        """
        raise NotImplementedError("IChatLog.deserialize must be implemented")
