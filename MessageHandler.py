import random
import time

import Event
import requests
import Judge


def sendMessage(send_message):
    """ 向用户发送消息 """
    # 构造发送消息的URL
    url = 'http://127.0.0.1:3000' + send_message.getPostUrl()
    # 确保消息发送间隔，避免过于频繁
    time.sleep(1 + random.random())
    # 发送消息并获取响应
    responses = requests.post(url=url, json=send_message.ToMessage())
    # 打印响应内容
    print(responses.json())


def MessageHandler(recv_msg):
    """ 消息处理 """
    # 初始化发送的消息为None
    send_msg = None
    # 如果接收到的消息是@我，则调用插件事件处理
    if Judge.isAtMe(recv_msg):
        send_msg = Event.plugin_event['gpt']['event'].pluginRun(recv_msg)
    # 如果是命令，回复特定命令使用信息
    elif Judge.isComment(recv_msg):
        send_msg = Event.run(recv_msg)

    # 如果有消息需要发送，则调用sendMessage函数发送
    if send_msg is not None:
        sendMessage(send_msg)
