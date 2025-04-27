from ...defs.ctrldef import SingleChatHistory

class IChatHistory:
    def __init__(self, config: dict):
        self.config = config

    def get_chat_history(self, chat_id: str) -> SingleChatHistory:
        raise NotImplementedError("Must implement at derived class")

    def create_chat(self, chat_id: str, chat_data: SingleChatHistory):
        raise NotImplementedError("Must implement at derived class")

    def is_exists(self, chat_id: str) -> bool:
        raise NotImplementedError("Must implement at derived class")

    def serialize(self):
        raise NotImplementedError("Must implement at derived class")

    def deserialize(self):
        raise NotImplementedError("Must implement at derived class")
