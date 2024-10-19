import itchat

from config.config import ROLE
from logs.logger import logger
from session.session import sessions

def keyboard_exception():
    while True:
        try:
            end_order = input("终止程序请输入exit:\n")
            if end_order == "exit":
                raise KeyboardInterrupt
        except KeyboardInterrupt as e:
            if sessions != {}:
                for session in sessions.values():
                    itchat.send(f"【程序被终止,{ROLE}已下线。】", toUserName=session.user_name)
            logger.debug("程序正常关闭。")
            return

