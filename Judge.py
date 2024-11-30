import Message

def isAtMe(message) -> bool:
    """ 判断是否被at """
    messages = message.getMessage()
    msg = messages[0]
    if msg.get('type') == 'at' and \
            msg.get('data').get('qq') == message.getSelfId():
        return True
    return False


def isComment(message) -> bool:
    """ 判断是否是命令 """
    messages = message.getRawMessage().split(' ')
    for msg in messages:
        if msg[0] == '/':
            return True
    return False
