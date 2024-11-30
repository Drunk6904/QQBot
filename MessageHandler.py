import time
import Message
import requests
import Judge
import gpt


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
    """
    处理通过私聊发送来的消息
    """
    if recv_msg.getRawMessage() == '/help':
        # 回复帮助
        send_msg = Message.SendMessage(id=recv_msg.getMessageSenderId(), message_type='private')
        send_msg.AddMessageData('text', "help")
        sendMessage(send_msg)


def groupMessageHandler(recv_msg):
    """
    处理通过群聊发送来的消息
    :param recv_msg: 接收到的消息对象
    :return:
    """

    if recv_msg.getRawMessage() == '/help':
        # 回复帮助
        send_msg = Message.SendMessage(id=recv_msg.getGroupId(), message_type='group')
        send_msg.AddMessageData('text', "help")
        sendMessage(send_msg)
    elif Judge.isAtMe(recv_msg):
        # gpt回复
        send_msg = Message.SendMessage(id=recv_msg.getGroupId(), message_type='group')
        send_msg.AddMessageData('at', recv_msg.getSenderId())

        post_gpt_message = recv_msg.getRawMessage().split(" ")[1]
        gpt_message = gpt.post_message(post_gpt_message)
        send_msg.AddMessageData('text', " " + gpt_message)
        sendMessage(send_msg)
