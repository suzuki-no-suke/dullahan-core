from dullahan.system.Factory_SystemFileProvider import Factory_SystemFileProvider
from dullahan.system.LoadSystemConfig import LoadSystemConfig

sys_conf_path = "./asset/system_config.xml"

sys_conf = LoadSystemConfig.load(sys_conf_path)
sys_provider = Factory_SystemFileProvider.create(sys_conf)

names = []
content_lines = []

for botname, conf in sys_provider.bot_regist.bot_configs.items():
    names.append(botname)
    content_lines.append(f"# {botname}")
    content_lines.append(f"- ベースBOT : {conf['profile']['basemodel']}")
    content_lines.append(f"- バージョン : {conf['profile']['version']}")
    content_lines.append(f"")
    content_lines.append(f"{conf['profile']['description']}")
    if 'prompts' in conf and 'guidance' in conf['prompts']:
        content_lines.append(f"")
        content_lines.append(f"(guidance)")
        content_lines.append(conf['prompts']['guidance'])
    content_lines.append(f"")
    content_lines.append(f"")

headers = []
headers.append(f"BOT LIST")
headers.append(f"=================")
headers.append(f"")
headers.append(f"# Bot names")
for n in names:
    headers.append(f" - {n}")
headers.append(f"")
headers.append(f"")
headers.append(f"")

with open("./datakeep/Bots.md", "w", encoding="utf-8") as f:
    f.write("\n".join(headers))
    f.write("\n".join(content_lines))

