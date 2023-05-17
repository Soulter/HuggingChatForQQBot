from nakuru.entities.components import *
from nakuru import (
    GroupMessage,
    FriendMessage
)
from botpy.message import Message, DirectMessage
from hugchat import hugchat

class HuggingChatForQQBotPlugin:
    """
    初始化函数, 可以选择直接pass
    """
    def __init__(self) -> None:
        self.chatbot = hugchat.ChatBot(cookie_path = "cookies_hc.json")
        print("启动HuggingChatForQQBot插件")


    """
    入口函数，机器人会调用此函数。
    参数规范: message: 消息文本; role: 身份; platform: 消息平台; message_obj: 消息对象
    参数详情: role为admin或者member; platform为qqchan或者gocq; message_obj为nakuru的GroupMessage对象或者FriendMessage对象或者频道的Message, DirectMessage对象。
    返回规范: bool: 是否hit到此插件(所有的消息均会调用每一个载入的插件, 如果没有hit到, 则应返回False)
             Tuple: None或者长度为3的元组。当没有hit到时, 返回None. hit到时, 第1个参数为指令是否调用成功, 第2个参数为返回的消息文本或者gocq的消息链列表, 第3个参数为指令名称
    例子：做一个名为"yuanshen"的插件；当接收到消息为“原神 可莉”, 如果不想要处理此消息，则返回False, None；如果想要处理，但是执行失败了，返回True, tuple([False, "请求失败啦~", "yuanshen"])
          ；执行成功了，返回True, tuple([True, "结果文本", "yuanshen"])
    """
    def run(self, message: str, role: str, platform: str, message_obj, qq_platform = None):

        if platform == "gocq":
            """
            QQ平台指令处理逻辑
            """
            if message.startswith("hc "):
                res = self.chatbot.chat(message[3:])
                if res != "":
                    return True, tuple([True, [Plain(res)], "HuggingChatForQQBot"])
                else:
                    return True, tuple([False, "响应结果为空~", "HuggingChatForQQBot"])
            else:
                return False, None
        elif platform == "qqchan":
            """
            频道处理逻辑(频道暂时只支持回复字符串类型的信息，返回的信息都会被转成字符串，如果不想处理某一个平台的信息，直接返回False, None就行)
            """
            if message.startswith("hc "):
                res = self.chatbot.chat(message[3:])
                if res != "":
                    return True, tuple([True, res, "HuggingChatForQQBot"])
                else:
                    return True, tuple([False, "响应结果为空~", "HuggingChatForQQBot"])
                
    """
    帮助函数，当用户输入 plugin v 插件名称 时，会调用此函数，返回帮助信息
    返回参数要求(必填)：dict{
        "name": str, # 插件名称
        "desc": str, # 插件简短描述
        "help": str, # 插件帮助信息
        "version": str, # 插件版本
        "author": str, # 插件作者
    }
    """        
    def info(self):
        return {
            "name": "HuggingChatForQQBot",
            "desc": "使用hugging-chat-api实现聊天功能",
            "help": "HuggingChatForQQBot插件，使用hugging-chat-api，实现聊天功能\n使用方法：先要获取cookies，方法见github.com/Soulter/hugging-chat-api，然后保存cookies到机器人目录下：新建文件cookies_hc.json，填进去\n\n发送 hc + 空格 + 消息，即可调用hugchat聊天功能",
            "version": "v1.0.2",
            "author": "Soulter"
        }

        # 热知识：检测消息开头指令，使用以下方法
        # if message.startswith("原神"):
        #     pass