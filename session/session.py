import queue
import threading
import time
import itchat

from config.config import *
from logs.logger import logger
from model import doubao

# 会话字典（初始值保持空值）
sessions = {}

class Session:
    def __init__(self, user_name):
        self.user_name = user_name
        self.messages = [{"role": "system", "content": SYSTEM_MSG}]
        self.in_session = False
        self.msg_queue = queue.Queue()
        self.thread = threading.Thread(target=self.process_messages)
        self.init_time = time.time()
        self.thread.start()

    def process_messages(self):
        while True:
            # 监听信息（队列为空时阻塞线程）
            msg = self.msg_queue.get()
            if msg is None:
                break  # 跳出线程
            # 信息交由handle_message处理
            self.handle_message(msg)

    def handle_message(self, msg):
        if msg.Content == START_ORDER and not self.in_session:
            self.in_session = True
            itchat.send_msg(f"【{ROLE}已上线。】", toUserName=self.user_name)
            logger.debug("已开启和{}窗口的会话...".format(self.user_name))
            logger.debug("当前正在进行的会话："+str(sessions))
            return

        if msg.Content == EXIT_ORDER and self.in_session:
            self.in_session = False  # 关闭会话参数
            # 告知用户状态
            itchat.send_msg(f"【{ROLE}已下线。】", toUserName=self.user_name)
            # 流量监控
            self.flow_monitoring()
            # 将线程移出队列并返回检查
            self.msg_queue.put(None)
            time.sleep(0.5)  # 等队列消息处理完后安全关闭
            sessions.pop(self.user_name, None)
            # 控制台输出会话状态信息
            logger.debug("已结束和{}窗口的会话...".format(self.user_name))
            logger.debug("当前正在进行的会话："+str(sessions))
            return

        if msg.Content.startswith('/') and self.in_session:
            user_message = {"role": "user", "content": msg.Content.lstrip("/")}
            self.messages.append(user_message)
            ai_response = doubao.reply_by_assistant_single(self.messages,model_id=MODEL_ID)
            logger.debug("【Assistant】:"+ai_response)
            ai_message = {"role": "assistant", "content": ai_response}
            self.messages.append(ai_message)
            # 向用户窗口响应消息
            itchat.send_msg(f"{ROLE}：" + ai_response, toUserName=self.user_name)

    def flow_monitoring(self):
        # 日志记录流量监控
        messages_list = [content['content'] for content in self.messages]
        word_amount = sum([(len(messages_list[i]) * (len(messages_list) - i)) for i in range(len(messages_list))])
        record = f'Session{self.user_name} has used token(approximately)：{word_amount}'
        logger.info(record)