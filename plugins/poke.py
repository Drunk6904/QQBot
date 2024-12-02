import sys

import Notify

sys.path.append("../")

import Message

# 调用指令
comment = ["戳"]


def getAt(recv_msg):
    """
    判断是否被@
    """
    # 获取自己的QQ号码
    self_id = recv_msg.getSelfId()

    # 遍历接收到的消息列表，寻找是否有@类型的消息
    messages = recv_msg.getMessage()
    if not isinstance(messages, list):
        raise ValueError("getMessage() should return a list")

    for msg in messages:
        if not isinstance(msg, dict) or 'type' not in msg or 'data' not in msg:
            raise ValueError("Invalid message format")

        # 如果消息类型不是@，则跳过当前循环
        if msg['type'] != 'at':
            continue

        # 获取被@的QQ号码
        data = msg['data']
        if not isinstance(data, dict) or 'qq' not in data:
            raise ValueError("Invalid data format")

        reply_id = data['qq']

        # 如果被@的QQ号码是自己
        if reply_id == self_id:
            return {'is_self': True, 'reply_id': None}
        # 如果不是自己被@
        else:
            return {'is_self': False, 'reply_id': reply_id}
    # 如果没有被@
    return {'is_self': False, 'reply_id': None}


def pluginRun(recv_msg) -> Message.SendMessage:
    """
    插件运行入口，根据接收到的消息类型决定如何回复
    """

    # 判断接收到的消息类型是否为群聊消息
    if type(recv_msg) is Message.RecvMessage:
        if recv_msg.getMessageType() == Message.Message.GROUP_MESSAGE:
            # 如果是群聊消息，则检查是否有人被@
            group_id = recv_msg.getGroupId()
            at_info = getAt(recv_msg)
            print(at_info)
            # 根据at信息处理不同的消息发送逻辑
            send_msg = None
            if at_info['is_self']:
                # 如果是自己被戳，则发送特定消息
                send_msg = Message.SendMessage(group_id, Message.Message.GROUP_MESSAGE)
                send_msg.AddMessageData('text', 'o.O?')

            elif at_info['is_self'] is False and at_info['reply_id'] is None:
                # # 如果不是自己被戳且没有回复ID，则发送使用戳一戳功能的提示信息
                # send_msg = Message.SendMessage(group_id, Message.Message.GROUP_MESSAGE)
                # send_msg.AddMessageData('text', '戳一戳的格式为：/戳 @xx')
                pass

            elif at_info['is_self'] is False and at_info['reply_id'] is not None:
                # 如果不是自己被戳且有回复ID，则执行戳一戳操作
                send_msg = Message.SendMessage(group_id, Message.SendMessage.GROUP_POKE)
                send_msg.AddMessageData('group_poke', at_info['reply_id'])

            # 发送戳一戳消息
            return send_msg

    # 判断接收到的消息类型是否为通知消息
    elif type(recv_msg) is Notify.Notify:
        reply_id = recv_msg.getReplyId()
        reply_type = recv_msg.getReplyType()
        if reply_type == Message.SendMessage.GROUP_POKE:
            # 如果是群聊戳一戳
            send_msg = Message.SendMessage(reply_id, Message.SendMessage.GROUP_POKE)
            send_msg.AddMessageData(Message.SendMessage.GROUP_POKE, recv_msg.getUserId())
            return send_msg
        elif recv_msg.getReplyType() == Message.SendMessage.PRIVATE_POKE:
            # 如果是私聊戳一戳
            send_msg = Message.SendMessage(reply_id, Message.SendMessage.PRIVATE_POKE)
            return send_msg
