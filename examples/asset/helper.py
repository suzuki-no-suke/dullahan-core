from dullahan.system.Factory_SystemFileProvider import Factory_SystemFileProvider
from dullahan.provider.Factory_LocalFileProvider import LocalFileProvider
from dullahan.system.LoadSystemConfig import LoadSystemConfig
from dullahan.ChatSystem import ChatSystem

def prepare(system_config_path: str):
    config = LoadSystemConfig.load(system_config_path)
    sys_provider = Factory_SystemFileProvider.create(config)
    provider = LocalFileProvider.create(config)
    chatsys = ChatSystem(sys_provider, provider)
    return chatsys.generate_ctrl(), sys_provider, provider


from dullahan.defs.datadef import ChatLogData

def to_md(log: ChatLogData) -> str:
    lines = []
    
    # ヘッダー情報
    lines.append(f"{log.chat_title}")
    lines.append(f"===================================")
    lines.append(f"")
    lines.append(f"- チャットID: `{log.chat_id}`")
    lines.append(f"- システム: {log.system_name}")
    lines.append(f"- ステータス: {log.status}")
    lines.append(f"")
    lines.append(f"")
    
    # メッセージ一覧
    lines.append("## メッセージ一覧")
    lines.append("")
    
    for msg in log.messages:
        # メッセージヘッダー
        lines.append(f"### {msg.role} - {msg.subsystem_name}")
        lines.append(f"- メッセージID : {msg.message_id}")
        lines.append(f"- 作成日時: {msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}*")
        
        # メッセージ内容
        lines.append("")
        lines.append(msg.message)
        lines.append("")
        lines.append(f"")

    return "\n".join(lines)

def write_to_md(filepath: str, log: ChatLogData):
    text = to_md(log)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

from dullahan.defs.datadef import ChatLogData

def print_log(chat_log: ChatLogData):
    for msg in chat_log.messages:
        print(f"{msg.role} - {msg.message}")
