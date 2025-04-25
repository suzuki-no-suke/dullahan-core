from asset.helper import *

sys_config_path = "./assets/file_config.xml"

ctrl, sys_prov, prov = prepare(sys_config_path)

chat_id = ctrl.create_chat("EchoBot_ContinualCall")
ctrl.opening(chat_id)

ctrl.chat(chat_id, "test yade")
ctrl.chat(chat_id, "つづきやで")

print_log(prov.logs.get_log(chat_id))
ctrl.close()
write_to_md("./md/25xxxx-test.md", prov.logs.get_log(chat_id))


ctrl.close()
