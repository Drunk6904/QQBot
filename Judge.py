def isAtMe(message) -> bool:
    """ 判断是否被at """
    messages = message.getMessage()
    msg = messages[0:0]
    if msg.get('type') == 'at' and \
            msg.get('data').get('qq') == message.getSelfId():
        return True
    return False
