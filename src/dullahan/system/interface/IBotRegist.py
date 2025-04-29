
class IBotRegist:
    def __init__(self, system_config: dict):
        self.system_config = system_config

    def load(self, system_name: str):
        """ボット設定を読み込む

        Returns:
            None

        Raises:
            ValueError: 設定情報が不正な場合
        """
        raise NotImplementedError("loadメソッドは継承先で実装する必要があります")

    def list_bot_names(self) -> list[str]:
        """
        ボット名を全て返す

        Returns:
            list[str]: 利用可能なボット名のリスト
        """
        raise NotImplementedError("loadメソッドは継承先で実装する必要があります")

    def get_config(self, system_name: str) -> dict:
        """指定されたボット名の設定を取得する

        Args:
            bot_name (str): ボット名

        Returns:
            dict: ボットの設定情報

        Raises:
            KeyError: 指定されたボット名が見つからない場合
        """
        raise NotImplementedError("get_configメソッドは継承先で実装する必要があります")

    def is_exist(self, system_name: str):
        raise NotImplementedError("is_existメソッドは継承先で実装する必要があります")
