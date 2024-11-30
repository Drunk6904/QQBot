import time


class Notify:
    """
    通知事件类
    """
    time = None  # 时间
    self_id = None  # 机器人QQ号
    post_type = None    # 事件类型
    notice_type = None  # 通知类型
    sub_type = None     # 子类型
    target_id = None  # 目标ID，通常是被戳的人的QQ号
    user_id = None  # 发起戳一戳的用户的QQ号
    group_id = None  # 群号
    raw_info = None  # 原始信息

    def __init__(self, recv_notify):
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(recv_notify.get('time'))))  # 时间
        self.self_id = recv_notify.get('self_id')  # 机器人QQ号
        self.post_type = recv_notify.get('post_type')  # 事件类型
        self.notice_type = recv_notify.get('notice_type')  # 通知类型
        self.sub_type = recv_notify.get('sub_type')  # 子类型
        self.target_id = recv_notify.get('target_id')  # 目标ID，通常是被戳的人的QQ号
        self.user_id = recv_notify.get('user_id')  # 发起戳一戳的用户的QQ号
        self.group_id = recv_notify.get('group_id')  # 群号
        self.raw_info = recv_notify.get('raw_info')  # 原始信息

