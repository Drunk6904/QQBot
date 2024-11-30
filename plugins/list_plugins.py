import sys

import Event

sys.path.append("../")

import Message

# 调用指令
comment = ["plugin", "插件"]


def pluginRun(recv_msg, send_msg) -> Message.SendMessage:
    send_msg.AddMessageData('text', "目前装载插件:")
    for plugin in Event.plugin_event.keys():
        send_msg.AddMessageData('text', "\n" + plugin)
    return send_msg
