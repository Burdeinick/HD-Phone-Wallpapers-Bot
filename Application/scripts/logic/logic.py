import json
import sqlite3
import requests
from logger.log import MyLogging
from TOKEN import token, my_chat_id


super_logger = MyLogging().setup_logger('logic',
                                        'Application/logger/logfile.log')


def send_error_message():
    """The function can send message that have error."""
    try:
        method = "sendMessage"
        text = f"Что-то рухнуло иди смотреть в logfile.log"
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"chat_id": my_chat_id, "text": text}
        requests.post(url, data=data)

    except Exception:
        super_logger.error('Error send_message', exc_info=True)


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
        """The function returns True if new user
        added to DB else returns False.

        """
        try:
            request = f"""INSERT INTO user(user_id,
                                           status_start,
                                           status_take_iphone)
                          VALUES({user_id}, 1, 0)
                       """
            self.conn.execute(request)
            self.conn.commit()
            return True

        except Exception:
            super_logger.error('Error add_user_info', exc_info=True)
            send_error_message()
            return False

    def get_user_info(self, user_id: str) -> list:
        """The function returns info about one user."""
        try:
            request = f"""SELECT user_id,
                                 id_iphone,
                                 status_start,
                                 status_take_iphone
                          FROM user
                          WHERE user_id = '{user_id}'
                       """
            self.cursor.execute(request)
            return self.cursor.fetchall()

        except Exception:
            super_logger.error('Error get_user_info', exc_info=True)
            send_error_message()

    def get_iphone_info(self) -> list:
        """The function returns info list about 'iphone'."""
        try:
            request = f"""SELECT title, id_iphone
                          FROM iphone
                          ORDER BY id_iphone DESC
                       """
            self.cursor.execute(request)
            return self.cursor.fetchall()

        except Exception:
            super_logger.error('Error get_iphone_info', exc_info=True)
            send_error_message()

    def set_status_take_iphone(self, user_id) -> bool:
        """The function returns True if 'status_take_iphone'
        successfully set to True.

        """
        try:
            request = f"""UPDATE user
                          SET status_take_iphone = 1
                          WHERE user_id = {user_id}
                       """
            self.conn.execute(request)
            self.conn.commit()
            return True

        except Exception:
            super_logger.error('Error', exc_info=True)
            send_error_message()
            return False

    def set_id_iphone(self, user_id: str, text_message: str) -> bool:
        """The function returns True if request with
        SET 'id iphone' end successfully.

        """
        try:
            request = f"""UPDATE user
                          SET id_iphone = (
                                            SELECT id_iphone
                                            FROM iphone
                                            WHERE title = '{text_message}'
                                            )
                          WHERE user_id = {user_id}
                       """
            self.conn.execute(request)
            self.conn.commit()
            return True

        except Exception:
            super_logger.error('Error set_id_iphone', exc_info=True)
            send_error_message()
            return False

    def get_pixresolution(self, user_id: str) -> list:
        """The function returns value resolution of
        need iphone model for it user.

        """
        try:
            request = f"""SELECT val
                            FROM pixresolution JOIN
                            iphone USING(id_pixresolution)
                            JOIN user USING(id_iphone)
                            WHERE user_id = {user_id}
                       """
            self.cursor.execute(request)
            return self.cursor.fetchall()

        except Exception:
            super_logger.error('Error get_iphone_info', exc_info=True)
            send_error_message()

    def del_user(self, user_id: str) -> bool:
        """The function returns True if user was
        successfully deleted of DB else False.

        """
        try:
            request = f"""DELETE FROM user
                          WHERE user_id = {user_id}
                       """
            self.conn.execute(request)
            self.conn.commit()
            return True

        except Exception:
            super_logger.error('Error del_user', exc_info=True)
            send_error_message()
            return False

    def get_all_users(self) -> list:
        """The function returns return list with number of users."""
        try:
            request = f"""SELECT COUNT(*) FROM user"""
            self.cursor.execute(request)
            return self.cursor.fetchall()

        except Exception:
            super_logger.error('Error get_all_users', exc_info=True)
            send_error_message()


class Telegram:
    """The class for work with Telegram API."""
    def __init__(self):
        self.request_db = RequestsDb()
        self.hand_req_db = HandlerReqDb()

    async def send_message(self, chat_id, text):
        """The function can send message necessary user."""
        try:
            method = "sendMessage"
            url = f"https://api.telegram.org/bot{token}/{method}"
            data = {"chat_id": chat_id, "text": text}
            requests.post(url, data=data)

        except Exception:
            super_logger.error('Error send_message', exc_info=True)
            send_error_message()

    def select_iphone(self, user_id):
        """The function can call function for send buttons to
        user with all exists to DB of  iPhone model.

        """
        try:
            get_info = self.request_db.get_iphone_info()
            lst_iphones = self.hand_req_db.hand_iphone_info(get_info)
            text = "Выберете модель Вашего iPhone 👇🏻"
            self.button(lst_iphones, user_id, text=text)

        except Exception:
            super_logger.error('Error select_iphone', exc_info=True)
            send_error_message()

    def chang_iph(self, user_id, text="Отлично! Я запомнил данную модель 😎"):
        """The function can call function for send buttons
        'Получить обои' and 'Изменить модель iphone'.

        """
        try:
            title_button = [
                            [{"text": "Получить обои"}],
                            [{"text": "Изменить модель iPhone"}]
                            ]
            self.button(title_button, user_id, text)

        except Exception:
            super_logger.error('Error get_picture_chang_iph', exc_info=True)
            send_error_message()

    def get_start_butt(self, user_id, text):
        """The function can call function for send button 'Начать'."""
        try:
            title_button = [[{"text": "Начать"}]]
            self.button(title_button, user_id, text)

        except Exception:
            super_logger.error('Error get_start_butt', exc_info=True)
            send_error_message()

    def button(self, title_button: list, user_id: str, text="👌"):
        """The function can do request to
        telegram API for send buttons user.

        """
        try:
            method = "sendMessage"
            url = f"https://api.telegram.org/bot{token}/{method}"
            bt = {"keyboard": title_button, "resize_keyboard": True}
            reply = json.dumps(bt)
            params = {"chat_id": user_id, "reply_markup": reply, "text": text}
            requests.post(url, params)

        except Exception:
            super_logger.error('Error button', exc_info=True)
            send_error_message()


class HandlerReqDb:
    """The class can to do requests to DB and  handle responses."""
    def __init__(self):
        """The method creates instances of classes
        'ConnectionDB().conn' and 'RequestsDb()' for further use.

        """
        self.connect_db = ConnectionDB().conn
        self.request_db = RequestsDb()

    def hand_iphone_info(self, iphone_info: list) -> list:
        """The function folds all  the models iphone
        of DB and send их for display in Telegram.

        """
        try:
            buttons_lst = []
            for i in iphone_info:
                title_iphone = i[0]
                buttons_lst.append([{"text": f"{title_iphone}"}])
            return buttons_lst

        except Exception:
            super_logger.error('Error hand_iphone_info', exc_info=True)
            send_error_message()

    def user_exist(self, user_id: str) -> bool:
        """The function return 'True' if user exist to DB."""
        try:
            user_info = self.request_db.get_user_info(user_id)
            if user_info:
                return True
            return False

        except Exception:
            super_logger.error('Error user_exist', exc_info=True)
            send_error_message()
            return False

    def get_iphone_list(self) -> list:
        """The function return list of title iPhone model."""
        try:
            iphone_info = self.request_db.get_iphone_info()
            iphone_list = [i[0] for i in iphone_info]
            return iphone_list

        except Exception:
            super_logger.error('Error get_iphone_list', exc_info=True)
            send_error_message()

    def get_status_take_iphone(self, user_id: str) -> bool:
        """The function return 'True' if
        'status_take_iphone' of 'user' table == 1.

        """
        try:
            user_info = self.request_db.get_user_info(user_id)
            if user_info:
                status_take_iphone = user_info[0][3]
                if status_take_iphone:
                    return True
                return False

        except Exception:
            super_logger.error('Error get_status_take_iphone', exc_info=True)
            send_error_message()

    async def hand_get_pixresolution(self, chat_id) -> tuple:
        """The function parses resolution of
        iPhone and return tuple with two values resolution.

        """
        try:
            all_pix = self.request_db.get_pixresolution(chat_id)
            if all_pix:
                ferst_pix = all_pix[0][0].split(' ')[0]
                second_pix = all_pix[0][0].split(' ')[1]
                return (ferst_pix, second_pix)

        except Exception:
            super_logger.error('Error hand_get_pixresolution', exc_info=True)
            send_error_message()


class HandlerServer:
    """The class can to process requests
    regarding the text that is written in them.

    """
    def __init__(self, request_json):
        """This constructor creates instances classes
        "RequestsDb()", "HandlerReqDb()",
        "Telegram()" for further use and
        parsers request_json at  text_message, chat_id.

        """
        self.request_db = RequestsDb()
        self.hand_req_db = HandlerReqDb()
        self.teleg = Telegram()
        self.chat_id = request_json["message"]["chat"]["id"]
        self.text_message = request_json["message"]["text"] if "text" in request_json["message"] else ""

    def start_command(self):
        """The function run when getting "/start" command or "начать"."""
        try:
            user_exist = self.hand_req_db.user_exist(self.chat_id)
            if not user_exist:
                add_user = self.request_db.add_user_info(self.chat_id)
                if add_user:
                    self.teleg.select_iphone(self.chat_id)
            else:
                status_take_iphone = self.hand_req_db.get_status_take_iphone(self.chat_id)
                if status_take_iphone:
                    text = "Вы уже запустили бота 👌"
                    self.teleg.chang_iph(self.chat_id, text=text)
                else:
                    self.teleg.select_iphone(self.chat_id)

        except Exception:
            super_logger.error('Error start_command', exc_info=True)
            send_error_message()

    def any_iphon_command(self):
        """The function run when getting  commands any name iphone из DB."""
        try:
            user_exist = self.hand_req_db.user_exist(self.chat_id)
            if user_exist:
                stat_take_iphone = self.request_db.set_status_take_iphone(self.chat_id)
                set_id_iphone = self.request_db.set_id_iphone(self.chat_id, self.text_message)
                if stat_take_iphone and set_id_iphone:
                    text = "Модель iPhone успешно выбранна 👌"
                    self.teleg.chang_iph(self.chat_id, text=text)

        except Exception:
            super_logger.error('Error any_iphon_command', exc_info=True)
            send_error_message()

    def stop_command(self):
        """The function run when getting "/stop" command."""
        try:
            del_user = self.request_db.del_user(self.chat_id)
            if del_user:
                text = f"""Если Вы вновь захотите воспользоваться ботом,
                           нажмите - "Начать" 👇🏻"""
                self.teleg.get_start_butt(self.chat_id, text)

        except Exception:
            super_logger.error('Error stop_command', exc_info=True)
            send_error_message()

    async def chec_det_wal(self, text_message, chat_id):
        """The function run when getting "Получить обои" command."""
        try:
            if text_message == "Получить обои":
                user_exist = self.hand_req_db.user_exist(chat_id)
                stat_take_iphone = self.request_db.set_status_take_iphone(chat_id)
                if user_exist and stat_take_iphone:
                    return True
                return False

        except Exception:
            super_logger.error('Error chec_det_wal', exc_info=True)
            send_error_message()

    async def my_users(self, chat_id):
        """The function call function of sending messages to user."""
        try:
            user_exist = self.hand_req_db.user_exist(self.chat_id)
            if user_exist:
                numb_users = self.request_db.get_all_users()[0][0]
                text = f"Количество пользователей бота: {numb_users}"
                await self.teleg.send_message(chat_id, text=text)

        except Exception:
            super_logger.error('Error my_users', exc_info=True)
            send_error_message()

    async def select_comand(self):
        """The function chooses regarding "text_message" that do further."""
        try:
            if self.text_message == "/start" or self.text_message == "Начать":
                self.start_command()

            if self.text_message in self.hand_req_db.get_iphone_list():
                self.any_iphon_command()

            if self.text_message == "Изменить модель iPhone":
                self.teleg.select_iphone(self.chat_id)

            if self.text_message == "/stop":
                self.stop_command()

            if self.text_message == "/users":
                await self.my_users(self.chat_id)

        except Exception:
            super_logger.error('Error select_comand', exc_info=True)
            send_error_message()
