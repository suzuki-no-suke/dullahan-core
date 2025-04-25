import importlib
import sys

from ..provider.FunctionProvider import FunctionProvider

from ..defs.botdef import IBotBase

class SpawnBot:
    @classmethod
    def spawn(self, bot_config: dict, provider: FunctionProvider, chat_id: str) -> IBotBase:
        # 設定ファイルを読み込み
        basemodel = bot_config['profile']['basemodel']
        classname = basemodel.split('.')[-1]

        # BOTクラスを読み込み
        try:
            # モジュールがすでに読み込み済みの場合は再読み込み
            if basemodel in sys.modules:
                importlib.reload(sys.modules[basemodel])
            
            # モジュールを動的にインポート
            bot_module = importlib.import_module(basemodel)
            bot_class = getattr(bot_module, classname)

            # ボットインスタンスを生成
            bot_instance = bot_class(provider, chat_id, bot_config)
            return bot_instance
        except ImportError as imex:
            error_message = f"モジュールの読み込みに失敗しました: {basemodel}"
            raise ImportError(f"{error_message}: {str(imex)}") from imex
        except AttributeError as atex:
            error_message = f"{classname} クラスが見つかりません: {basemodel}"
            raise AttributeError(f"{error_message}: {str(atex)}") from atex

