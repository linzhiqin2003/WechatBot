import os.path
from datetime import datetime
import itchat
import pandas as pd

from config.config import MYNAME
from logs.logger import logger

class InitLogin:
    def __init__(self,username):
        self.login = itchat.auto_login(hotReload=True)
        self.users = itchat.get_friends()
        self.username = username
        self.DIR = os.path.dirname(os.path.abspath(__file__))
        self.CSV_DIR = os.path.join(self.DIR, "data")
        self.CSV_PATH = os.path.join(self.CSV_DIR, "userlist.csv")
        self.createdir = self.__create_dir()

    def __create_dir(self):
        if not os.path.exists(self.CSV_DIR):
            os.mkdir(self.CSV_DIR)
        logger.debug("^^登陆成功^^")

    def __user_parse(self):
        user_list = []
        for user in self.users:
            user_list.append([user.UserName, user.NickName])
        pd.DataFrame(user_list, columns=["username", "nickname"]).to_csv(self.CSV_PATH, index=False)
        return

    def __user_info_record(self):
        if not os.path.exists(self.CSV_PATH):
            self.__user_parse()
            logger.debug(f"{datetime.now()}\t用户信息表创建成功...")
        else:
            df = pd.read_csv(self.CSV_PATH)
            try:
                if df[df["username"] == self.users[0].UserName]["nickname"].iloc[0] == self.users[0].NickName:
                    pass
            except:
                self.__user_parse()
                logger.debug(f"{datetime.now()}\t用户信息表更新(覆盖原表)...")

    def my_info(self):
        self.__user_info_record()
        df = pd.read_csv(self.CSV_PATH)
        my_username = df[df["nickname"] == self.username]["username"].iloc[0]
        user_dic = {user["username"]: user["nickname"] for user in df.T.to_dict().values()}
        return my_username,user_dic

my_username,user_dic = InitLogin(MYNAME).my_info()