import time


class Message:
    """
    消息类，用于封装消息
    """

    def __init__(self, message=None, id=None, message_type=None):
        """
        初始化消息类
        :param id: 消息发送者id
        :param message_type: 消息类型
        """
        # 如果传入的是接收到的消息
        if message is not None:
            self.message = message.get('raw_message')
            self.sender = message.get('sender')  # 消息发送者id
            self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(message.get('time'))))  # 消息发送时间
            self.message_type = message.get('message_type')  # 消息类型
            self.user_id = None
            self.group_id = None
            if message_type == "group":
                self.group_id = message.get('group_id')
            elif message_type == "private":
                self.user_id = message.get('user_id')
        # 如果传入的是发送的消息
        elif id is not None and message_type is not None:
            self.id = id
            self.message_type = message_type
            self.message = list()

    def getMessageType(self):
        # 获取消息类型
        return self.message_type

    def getMessage(self):
        # 获取消息内容
        return self.message

    def getMessageSender(self):
        # 获取消息发送者
        return self.sender

    def getMessageTime(self):
        # 获取消息发送时间
        return self.time

    def getMessageGroupId(self):
        # 获取群号
        return self.group_id

    def getSendMessageUserId(self):
        # 获取发送者id
        if self.message_type == "private":
            return self.user_id
        elif self.message_type == "group":
            return self.getMessageSender().get('user_id')

    def addMessageData(self, type, data):
        """
        添加消息数据
        :param type: 消息类型
        :param data: 消息数据
        :return:
        """
        datatype = "text"
        if type in ["image", "video", "record"]:  # 图片 视频 语音
            datatype = "file"
        if type == "text":  # 文本
            datatype = "text"
        if type == "at":  # at
            datatype = "qq"
        if type == "face":  # 表情包
            datatype = "id"
        if type == "json":  # json
            datatype = "data"

        self.message.append(
            {
                "type": type,
                "data": {
                    datatype: data
                }
            }
        )

    def ToJson(self):
        """
        将消息转换为json格式
        :return: json格式的消息
        """
        message_type = self.message_type
        if message_type == "private":
            message_type = "user"
        return {
            f"{message_type}_id": self.id,
            "message": self.message
        }

    def getPostUrl(self):
        """
        获取消息发送的url
        :return:
        """
        if self.message_type == "group":
            return "/send_group_msg"
        if self.message_type == "private":
            return "/send_private_msg"
        print("error message type")

