import sys

sys.path.append("../")

import Message

# 调用指令
comment = ["test"]


def pluginRun(recv_msg) -> Message.SendMessage:
    """
    处理接收到的消息并生成回复消息。

    参数:
    recv_msg: 接收到的消息对象，包含消息的各种信息。

    返回:
    Message.SendMessage: 准备发送的回复消息对象。
    """
    # 创建回复消息对象
    send_msg = Message.SendMessage.createSendMessage(recv_msg)
    send_msg.AddMessageData('text', 'txt')

    # 返回构建好的回复消息对象
    return send_msg
