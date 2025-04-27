from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

class DbSession:
    """SQL Alchemy のSessionを管理する
    with構文で使用することを想定されたクラス

    使用例:
        with dbconn.session() as sess:
            # sessを使用してDB操作を行う
            pass

    """
    def __init__(self, dbobj):
        self.dbobj = dbobj
        self.session = None

    def __enter__(self):
        if self.session is not None:
            self.session.close()
            self.session = None
        session = sessionmaker(bind=self.dbobj.engine)()
        self.session = session
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.session is not None:
            self.session.close()
            self.session = None


class DBConnection:
    """SQLAlchemy の接続を管理するクラス"""
    def __init__(self, db_uri):
        self.db_uri = db_uri
        echoflag = os.getenv('DEBUG_QUERY_ECHO', False) == "True"
        self.engine = create_engine(self.db_uri, echo=echoflag)

    @classmethod
    def default_env(cls):
        """デフォルトの環境変数から接続を作成する"""
        load_dotenv()
        db_uri = os.getenv("DB_CONN")
        return cls(db_uri)

    def get_engine(self):
        return self.engine

    def get_new_session(self):
        return DbSession(self)

