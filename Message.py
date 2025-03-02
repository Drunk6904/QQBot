import time

import Notify


class MessageError(Exception):
    """消息错误类，用于处理消息错误"""

    def __init__(self, message):
        self.message = message


class Message:
    """
    消息类，用于封装消息
    """
    GROUP_MESSAGE = 'group'
    PRIVATE_MESSAGE = 'private'
    MESSAGE_TYPE = [GROUP_MESSAGE, PRIVATE_MESSAGE]  # 消息类型
    message = None
    raw_message = None

    def __init__(self, raw_message=None, message=None):
        self.message = message
        self.raw_message = raw_message

    def getMessage(self):
        # 获取消息内容
        return self.message


class RecvMessage(Message):
    """
    接收到的消息类
    """

    message_type = None  # 消息类型 - 群聊消息/私聊消息
    self_id = None  # 接收消息账号id
    sender = None  # 消息发送者
    sender_id = None  # 消息发送者id
    sender_name = None  # 消息发送者名称
    message_card = None  # 消息发送者群名片
    time = None  # 消息发送时间
    group_id = None  # 群号

    def __init__(self, message=None):
        """ 初始化消息类 """
        self.message_type = message.get('message_type')  # 消息类型
        if message.get('message_type') not in self.MESSAGE_TYPE:
            # 如果消息类型错误，抛出异常
            raise MessageError("message type error")

        super().__init__(raw_message=message.get('raw_message'), message=message.get('message'))  # 消息
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(message.get('time'))))  # 消息发送时间
        self.sender = message.get('sender')  # 消息发送者
        self.sender_id = message.get('sender').get('user_id')  # 消息发送者id
        self.sender_name = message.get('sender').get('nickname')  # 消息发送者名称
        self.message_card = message.get('sender').get('card')  # 消息发送者群名片
        self.self_id = message.get('self_id')  # 自己的id
        if self.message_type == 'group':
            # 如果该消息来自群聊，补充群号属性
            self.group_id = message.get('group_id')

    def getMessageType(self):
        # 获取消息类型
        return self.message_type

    def getRawMessage(self):
        # 获取原始消息
        return self.raw_message

    def getMessageSender(self):
        # 获取消息发送者
        return self.sender

    def getGroupId(self):
        # 获取群号
        return self.group_id

    def getMessageSenderId(self):
        # 获取消息发送者id
        return self.sender_id

    def getSelfId(self):
        # 获取自己的账号
        return str(self.self_id)

    def getSenderId(self):
        # 获取发送者id
        return self.sender_id

    def getMessageSenderName(self):
        # 获取消息发送者名称
        return self.sender_name

    def getMessageCard(self):
        # 获取消息发送者群名片
        return self.message_card

    def getMessageTime(self):
        # 获取消息发送时间
        return self.time

    def getComment(self):
        """ 获取消息中的指令 """
        for cmd in self.raw_message.split(' '):
            if cmd[0] == '/':
                return cmd[1:]
        return None


class SendMessage(Message):
    """
    发送的消息类
    """

    POST_URL = {
        'group': '/send_group_msg',
        'private': '/send_private_msg',
        'group_poke': '/group_poke',
        'private_poke': '/friend_poke'
    }
    GROUP_POKE = 'group_poke'
    PRIVATE_POKE = 'private_poke'
    message_type = None
    user_id = None  # 发送目标id
    group_id = None  # 群号

    def __init__(self, id, message_type):
        """ 初始化消息类 """
        super().__init__(message=list())
        self.message_type = message_type
        if message_type in ["group", "group_poke"]:
            self.group_id = id
        elif message_type in ["private", "private_poke"]:
            self.user_id = id

    def ToMessage(self):
        """
        获取完整的符合发送格式的消息 - json
        根据消息类型返回不同的消息体
        """
        if self.message_type == "group":
            return {
                "group_id": self.group_id,
                "message": self.message
            }
        elif self.message_type == "private":
            return {
                "user_id": self.user_id,
                "message": self.message
            }
        elif self.message_type == "group_poke":
            return {
                "group_id": self.group_id,
                "user_id": self.user_id
            }
        elif self.message_type == "private_poke":
            return {
                "user_id": self.user_id
            }
        return None

    def AddMessageData(self, type, data):
        """
        添加消息数据
        根据不同的消息类型，构造相应的消息数据结构
        """
        if type == "text":
            self.message.append(
                {
                    "type": type,
                    "data": {
                        "text": data
                    }
                }
            )
        if type == "at":
            self.message.append(
                {
                    "type": type,
                    "data": {
                        "qq": data
                    }
                }
            )
        if type == "face":
            self.message.append(
                {
                    "type": type,
                    "data": {
                        "id": data
                    }
                }
            )
        if type == "json":
            self.message.append(
                {
                    "type": type,
                    "data": {
                        "data": data
                    }
                }
            )
        if type == "image":
            self.message.append(
                {
                    "type": type,
                    "data": {
                        "file": data
                    }
                }
            )
        if type == "group_poke":
            self.user_id = data

    def getPostUrl(self):
        """
        获取发送消息的url
        根据消息类型返回对应的发送url
        """
        return self.POST_URL[self.message_type]

    @staticmethod
    def createSendMessage(recv_msg):
        """
        创建发送消息对象
        根据接收的消息对象，创建发送消息对象
        """
        # 初始化目标ID为空字符串
        target_id = ""
        send_msg = None
        if type(recv_msg) is RecvMessage:
            # 根据消息类型获取目标ID（群组ID或发送者ID）
            if recv_msg.getMessageType() == Message.GROUP_MESSAGE:
                target_id = recv_msg.getGroupId()
            elif recv_msg.getMessageType() == Message.PRIVATE_MESSAGE:
                target_id = recv_msg.getSenderId()
            send_msg = SendMessage(target_id, recv_msg.getMessageType())
        return send_msg

