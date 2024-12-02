import Message
import os
import sys
import importlib

import Notify

# 插件事件
plugin_event = {}
"""
    'name': {
        'comment': ['cmd'],
        'event': module
    }
"""


def load_plugins():
    """ 加载插件 """
    # 获取所有插件
    files = [plugin_name[:-3] for plugin_name in os.listdir("plugins") if plugin_name.endswith(".py")]
    for plugin_name in files:
        # 导入插件
        print("正在导入插件：" + plugin_name)
        try:
            mod = importlib.import_module("plugins." + plugin_name)

            # 检查插件是否定义了pluginRun函数和comment属性
            if not hasattr(mod, "pluginRun"):
                raise Exception("插件未定义pluginRun函数")
            if not hasattr(mod, "comment"):
                raise Exception("插件未定义comment属性")

            # 将插件的信息添加到plugin_event字典中
            plugin_event[plugin_name] = {"comment": mod.comment, "event": mod}

            print("导入插件成功：" + plugin_name)
        except Exception as e:
            # 如果导入失败，删除插件的引用并打印错误信息
            del plugin_event[plugin_name]
            print("导入插件失败：" + plugin_name)
            print(e)


def run(recv_msg) -> Message.SendMessage:
    """
    运行插件
    根据接收到的消息判断是否需要运行插件，并返回处理后的消息
    参数:
    recv_msg: 接收到的消息对象，用于判断是否匹配插件运行条件
    send_msg: 待发送的消息对象，由插件处理后可能被修改
    返回:
    Message.SendMessage: 处理后的消息对象，准备发送给用户
    """
    # 如果接收到的消息对象是RecvMessage，则判断是否需要运行插件
    if type(recv_msg) is Message.RecvMessage:
        # 提取接收到的消息中的评论内容
        comment = recv_msg.getComment()

        # 如果评论内容存在，则遍历所有插件事件，寻找匹配的插件
        if comment:
            for plugin in plugin_event.keys():
                # 如果评论内容在当前插件的触发评论列表中，则运行该插件
                if comment in plugin_event[plugin]["comment"]:
                    send_msg = plugin_event[plugin]['event'].pluginRun(recv_msg)
                    return send_msg
    # 如果接收到的消息对象是Notify类型
    elif type(recv_msg) is Notify.Notify:
        # 检查通知的子类型是否为poke（戳一戳），并且目标ID与自己的ID相同，并且不是自己发起的
        if recv_msg.getSubType() == 'poke' and \
                str(recv_msg.getTargetId()) == str(recv_msg.getSelfId()) and \
                recv_msg.getUserId() != recv_msg.getSelfId():  # 防止死循环
            # 调用相应的插件处理此消息，并将处理结果存储在send_msg变量中
            send_msg = plugin_event['poke']['event'].pluginRun(recv_msg)
            return send_msg


if __name__ == '__main__':
    load_plugins()
