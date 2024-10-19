import threading
import time

import itchat
from itchat.content import *

from config.config import *
from exceptions.exception import keyboard_exception
from login.logininit import my_username, user_dic
from session.session import Session,sessions
from logs.logger import logger

@itchat.msg_register([TEXT], isFriendChat=True,isGroupChat=True)
def assist_chat(msg):
    if (msg.CreateTime + 3) > int(time.time()):  # 确认消息是线程开启后传来的，以免itchat的bug影响程序正常使用（保证会话进程列表安全）
        if msg.FromUserName == my_username: # 如果消息是我发的
            logger.debug("【我】:"+ msg.Content)
            user_name = msg.ToUserName
        else: #如果消息是别人发的话
            user_name = msg.FromUserName
            if user_name.startswith("@@"):
                logger.debug(f"【{msg.User.NickName}】："+msg.Content)
            else:
                logger.debug(f"【{user_dic[user_name]}】："+msg.Content)

        if msg.Content == START_ORDER:
            if user_name not in sessions: # 如果会话还没开启，则初始化
                sessions[user_name] = Session(user_name)
                #若会话开启，则上传消息给session对象
                session = sessions[user_name]
                session.msg_queue.put(msg)

        if user_name in sessions: #如果会话已开启
            session = sessions[user_name]
            session.msg_queue.put(msg)

def chat_run():
    itchat.run()


if __name__ == '__main__':
    threading.Thread(target=chat_run,daemon=True).start()
    logger.debug(keyboard_exception())


