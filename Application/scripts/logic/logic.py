import json
import sqlite3
import requests
# import sys
# sys.path.insert(0, 'Application')
from logger.log import MyLogging
from TOKEN import token


super_logger = MyLogging().setup_logger('preparing_db_logger',
                                        'Application/logger/logfile.log')


class ConnectionDB:
    """Class for connect to DB."""
    def __init__(self):
        self.dbname = self.get_config_db()[0]
        self.conn = sqlite3.connect(self.dbname, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_config_db(self) -> tuple:
        """The method getting informations of configuration file."""
        with open('Application/config.json') as config:
            json_str = config.read()
            json_str = json.loads(json_str)
        dbname = str(json_str['data_base']['dbname'])
        return (dbname, )

class RequestsDb:
    """Class for requests DB.
    The query syntax is intended for working with the 'Sqlite' database.
    """
    def __init__(self):
        self.conn = ConnectionDB().conn
        self.cursor = ConnectionDB().cursor

    def add_user_info(self, user_id: str) -> bool:
        """ """
        try:
            request = f"""INSERT INTO user(user_id, status_start)
                          VALUES({user_id}, 1)
                       """
            self.conn.execute(request)
            self.conn.commit()
            return True

        except Exception:
            super_logger.error('Error', exc_info=True)
            return False


    def get_user_info(self, user_id: str) -> list:
        """ """
        try:
            request = f"""SELECT user_id, id_iphone, status_start, status_take_iphone
                          FROM user
                          WHERE user_id = '{user_id}'
                       """
            self.cursor.execute(request)
            return self.cursor.fetchall()

        except Exception:
            super_logger.error('Error get_user_id', exc_info=True)

    def get_iphone_info(self) -> list:
        """ """
        try:
            request = f"""SELECT title, id_iphone
                          FROM iphone
                          ORDER BY id_iphone DESC
                       """
            self.cursor.execute(request)
            return self.cursor.fetchall()

        except Exception:
            super_logger.error('Error get_iphone_info', exc_info=True)     


class Telegram:
    """ """
    def __init__(self):
        self.request_db = RequestsDb()
        self.hand_req_db = HandlerReqDb()

    def send_message(self, chat_id, text):
        try:
            method = "sendMessage"
            url = f"https://api.telegram.org/bot{token}/{method}"
            data = {"chat_id": chat_id, "text": text}
            requests.post(url, data=data)

        except Exception:
            super_logger.error('Error send_message', exc_info=True) 

    def select_iphone(self, user_id):
        """"""
        try:
            get_info = self.request_db.get_iphone_info()
            lst_iphones = self.hand_req_db.hand_iphone_info(get_info)
            self.button(lst_iphones, user_id)

        except Exception:
            super_logger.error('Error select_iphone', exc_info=True)

    def get_picture(self, user_id):
        """ """
        try:
            title_button = [[{"text": "Получить обои"}]]
            self.button(title_button, user_id)

        except Exception:
            super_logger.error('Error get_picture', exc_info=True)

    def button(self, title_button: list, user_id: str):
        """ """
        try:
            method = "sendMessage"
            url = f"https://api.telegram.org/bot{token}/{method}"
            reply = json.dumps({"keyboard": title_button, "resize_keyboard": True})
            params = {"chat_id": user_id, "reply_markup": reply, "text": "Ok"}
            a = requests.post(url, params)
            print(a.content)
        
        except Exception:
            super_logger.error('Error button', exc_info=True)


class HandlerReqDb:
    """ """
    def __init__(self):
        self.connect_db = ConnectionDB().conn

    def hand_iphone_info(self, iphone_info: list) -> list:
        """ """
        try:
            buttons_lst = []
            for i in iphone_info:
                title_iphone = i[0]
                buttons_lst.append([{"text": f"{title_iphone}"}])
            return buttons_lst
        
        except Exception:
            super_logger.error('Error hand_iphone_info', exc_info=True)
