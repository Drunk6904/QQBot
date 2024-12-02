import sys

import requests

sys.path.append("../")

import Message

# 调用指令
comment = ["gpt"]

# api请求地址
chat_api = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
model_api = "https://ark.cn-beijing.volces.com/api/v3/bots/chat/completions"
# 密钥
api_key = "25f4ce8b-e860-4f04-a75f-c3755fdb4f5b"
# 推理接入
# jtm = "ep-20241126201234-59jtm"
jtm = "ep-20241129130441-qd7h2"
# 智能体
model = "bot-20241129131045-hcfxv"
# 请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
MAX_TOKENS = 100


# 对话消息
# message = []


def message_format(role, content):
    # 构造消息格式
    return {"role": role, "content": content}


def post_message(content):
    message = [message_format("user", content)]
    # 请求体
    data = {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "messages": message
    }
    # 接受响应
    response = requests.post(url=model_api, headers=headers, json=data).json()
    print(response)
    response_content = response.get("choices")[0].get("message").get("content")
    # message.append(message_format("assistant", response_content))
    print('ai：' + response_content)
    return response_content


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

    # 对于群组消息，添加@发送者的数据
    if recv_msg.getMessageType() == Message.Message.GROUP_MESSAGE:
        send_msg.AddMessageData('at', recv_msg.getSenderId())
    # 提取消息内容以发送给GPT模型
    post_gpt_message = recv_msg.getRawMessage().split(" ")[1]

    # 通过GPT模型获取回复消息
    gpt_message = post_message(post_gpt_message)

    # 将GPT回复的消息添加到回复消息中
    send_msg.AddMessageData('text', '\n' + gpt_message)

    # 返回构建好的回复消息对象
    return send_msg


if __name__ == '__main__':
    while True:
        string = input("用户：")
        post_message(string)
        if string == "bye":
            break
