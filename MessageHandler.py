import time

import Event
import Message
import requests
import Judge


def checkAndReply(recv_msg):
    """
    检查消息类型 并交予相应函数
    """
    recv_msg = Message.RecvMessage(message=recv_msg)
    if recv_msg.getMessageType() == 'group':
        groupMessageHandler(recv_msg)
    if recv_msg.getMessageType() == 'private':
        privateMessageHandler(recv_msg)


def sendMessage(send_message):
    """
    向用户发送消息
    """
    url = 'http://127.0.0.1:3000' + send_message.getPostUrl()
    time.sleep(1)
    responses = requests.post(url=url, json=send_message.ToMessage())
    print(responses.json())


def privateMessageHandler(recv_msg):
    """处理通过私聊发送来的消息"""
    # 创建一个用于发送的消息对象，设置接收者ID和消息类型为私聊
    send_msg = Message.SendMessage(id=recv_msg.getMessageSenderId(), message_type='private')

    # 根据内容生成回复消息
    send_msg = insert_message(recv_msg, send_msg)

    if send_msg is not None:
        # 发送处理后的消息
        sendMessage(send_msg)


def groupMessageHandler(recv_msg):
    """
    处理通过群聊发送来的消息
    :param recv_msg: 接收到的消息对象
    :return:
    """
    # 创建回复消息对象
    send_msg = Message.SendMessage(id=recv_msg.getGroupId(), message_type='group')
    send_msg.AddMessageData('at', recv_msg.getMessageSenderId())
    send_msg.AddMessageData('text', "\n")
    # 生成消息内容
    send_msg = insert_message(recv_msg, send_msg)

    if send_msg is not None:
        # 发送处理后的消息
        sendMessage(send_msg)


def insert_message(recv_msg, send_msg):
    """    插入消息    """
    # 如果消息中@了机器人，则进行GPT回复
    if Judge.isAtMe(recv_msg):
        send_msg = Event.plugin_event['gpt']['event'].pluginRun(recv_msg, send_msg)
        return send_msg
    elif Judge.isComment(recv_msg):
        # 如果是评论命令，回复特定命令使用信息
        send_msg = Event.run(recv_msg, send_msg)
        return send_msg
    return None
