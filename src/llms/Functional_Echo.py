from ..defs.datadef import ChatMessageData

class Functional_Echo:
    @classmethod
    def call(cls, messages: list[ChatMessageData]) -> str:
        last_message = ""
        for msg in reversed(messages):
            if msg.role == "user":
                last_message = msg.message
                break
        return last_message

