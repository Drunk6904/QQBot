import sys

import Notify

sys.path.append("../")

import Message

# 调用指令
comment = ["戳"]


def isAt(send_msg, recv_msg):
    """
    判断是否被@
    """
    # 遍历接收到的消息列表，寻找是否有@类型的消息
    for msg in recv_msg.getMessage():
        # 如果消息类型不是@，则跳过当前循环
        if msg.get('type') != 'at':
            continue
        # 获取被@的QQ号码
        reply_id = msg.get('data').get('qq')
        # 如果被@的QQ号码是自己，则添加文本消息"戳我干嘛"
        if reply_id == recv_msg.getSelfId():
            send_msg = send_msg.AddMessageData('text', '戳我干嘛')
        else:
            # 如果不是自己被@，则发送戳一戳消息给被@的人
            send_msg = Message.SendMessage(recv_msg.getGroupId(), 'group_poke')
            send_msg.AddMessageData('group_poke', reply_id)
    return send_msg


def pluginRun(recv_msg, send_msg=None) -> Message.SendMessage:
    """
    插件运行入口，根据接收到的消息类型决定如何回复
    """

    # 判断接收到的消息类型是否为群聊消息
    if type(recv_msg) is Message.RecvMessage:
        if recv_msg.getMessageType() == 'group':
            # 如果是群聊消息，则检查是否有人被@
            send_msg = isAt(send_msg, recv_msg)
            # 发送戳一戳消息
            return send_msg

    # 判断接收到的消息类型是否为通知消息
    elif type(recv_msg) is Notify.Notify:
        if recv_msg.getReplyType() == 'group_poke':
            # 如果是群聊戳一戳，则发送相应的戳一戳消息
            send_msg = Message.SendMessage(recv_msg.getReplyId(), 'group_poke')
            send_msg.AddMessageData('group_poke', recv_msg.getUserId())
            return send_msg
        elif recv_msg.getReplyType() == 'private_poke':
            # 如果是私聊戳一戳，则发送相应的戳一戳消息
            send_msg = Message.SendMessage(recv_msg.getReplyId(), 'private_poke')
            return send_msg
    return send_msg
