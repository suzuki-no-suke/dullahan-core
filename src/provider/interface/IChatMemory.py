from typing import Dict

class IChatMemory:
    """チャットごとの記憶を管理するインターフェース"""
    def __init__(self, config: dict = None):
        self.config = config

    def load(self, chat_id: str) -> Dict:
        """指定されたチャットIDの記憶を復旧します
        
        Args:
            chat_id (str): チャットID
            
        Returns:
            Dict: チャットの記憶データ
        """
        raise NotImplementedError("need to implement")
    
    def save(self, chat_id: str, memory: Dict) -> None:
        """指定されたチャットIDの記憶を更新します
        
        Args:
            chat_id (str): チャットID
            memory (Dict): 更新する記憶データ
        """
        raise NotImplementedError("need to implement")
    
    def serialize(self) -> None:
        """データ全体を永続化します"""
        raise NotImplementedError("need to implement")

    def deserialize(self) -> None:
        """永続化したデータを復旧します"""
        raise NotImplementedError("need to implement")



