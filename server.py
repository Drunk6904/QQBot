from flask import *

import Message
import Event
import MessageHandler
from Notify import Notify

app = Flask(__name__)


# 定义一个处理首页POST请求的路由
@app.route('/', methods=['POST'])
def listen_message():
    """
    监听并处理 incoming messages.

    该函数首先接收发送到根路径的POST请求，并尝试将其解析为JSON格式的消息。
    然后，根据消息的类型（'message' 或 'notice'），它将执行不同的处理逻辑。
    """
    # 接收并解析请求体为JSON格式
    message = request.json
    # 打印接收到的消息，便于调试和日志记录
    print("接收到消息:" + str(message))

    # 检查消息类型，如果为message'，则尝试回复消息
    if message.get('post_type') == 'message':
        MessageHandler.checkAndReply(message)
    # 如果消息类型为notice'，则视为通知，并尝试运行相关事件
    elif message.get('post_type') == 'notice':
        # 将消息封装为Notify对象，以便进一步处理
        message = Notify(message)
        # 运行事件，并检查是否有消息需要发送
        msg = Event.run(message)
        # 如果有消息需要发送，则执行发送操作
        if msg is not None:
            MessageHandler.sendMessage(msg)
    # 返回HTTP响应，表示处理成功
    return "200 OK"


if __name__ == '__main__':
    Event.load_plugins()
    app.run(host='0.0.0.0', port=8080, debug=True)
