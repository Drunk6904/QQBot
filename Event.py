import Message
import os
import sys
import importlib

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


def run(recv_msg, send_msg) -> Message.SendMessage:
    recv_msg.getRawMessage()
    return send_msg


if __name__ == '__main__':
    load_plugins()
