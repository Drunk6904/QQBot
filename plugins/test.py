import sys

sys.path.append("../")

import Message

# 调用指令
comment = ["test"]



def pluginRun(recv_msg, send_msg) -> Message.SendMessage:
    send_msg.AddMessageData('text', "test")
    return send_msg
