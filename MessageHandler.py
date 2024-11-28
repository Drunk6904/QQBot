import time
import Message
import requests


def checkAndReply(recv_msg):
    """
    检查消息类型 并交予相应函数
    :param recv_msg: 接收到的消息字典
    :return:
    """
    recv_msg = Message.Message(message=recv_msg)
    if recv_msg.message_type == 'group':
        groupMessageHandler(recv_msg)
    if recv_msg.message_type == 'private':
        privateMessageHandler(recv_msg)


def sendMessage(send_message):
    """
    向用户发送消息
    """
    url = 'http://127.0.0.1:3000' + send_message.getPostUrl()
    time.sleep(1)
    responses = requests.post(url=url, json=send_message.ToJson())
    print(send_message.ToJson(), responses.json())


def privateMessageHandler(recv_msg):
    """
    处理通过私聊发送来的消息
    :param recv_msg: 接收到的消息字典
    :return:
    """
    if recv_msg.message == 'help':
        # 回复帮助
        send_msg = Message.Message(id=recv_msg.getSendMessageUserId(), message_type='private')
        send_msg.addMessageData('text', "help")
        sendMessage(send_msg)


def groupMessageHandler(recv_msg):
    """
    处理通过群聊发送来的消息
    :param recv_msg: 接收到的消息对象
    :return:
    """

    if recv_msg.message == 'help':
        # 回复帮助
        send_msg = Message.Message(id=recv_msg.getMessageGroupId(), message_type='group')
        send_msg.addMessageData('text', "help")
        sendMessage(send_msg)
