import json
import sqlite3
import requests
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
        """The function returns True if new user added to DB else returns False."""
        try:
            request = f"""INSERT INTO user(user_id, status_start, status_take_iphone)
                          VALUES({user_id}, 1, 0)
                       """
            self.conn.execute(request)
            self.conn.commit()
            return True

        except Exception:
            super_logger.error('Error add_user_info', exc_info=True)
            return False

    def get_user_info(self, user_id: str) -> list:
        """The function returns info about one user."""
        try:
            request = f"""SELECT user_id, id_iphone, status_start, status_take_iphone
                          FROM user
                          WHERE user_id = '{user_id}'
                       """
            self.cursor.execute(request)
            return self.cursor.fetchall()

        except Exception:
            super_logger.error('Error get_user_info', exc_info=True)

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

    def set_status_take_iphone(self, user_id) -> bool:
        """The function returns True if 'status_take_iphone' successfully set to True."""
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
            return False

    def set_id_iphone(self, user_id: str, text_message: str) -> bool:
        """The function returns True if request with SET 'id iphone' end successfully."""
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
            return False

    def get_pixresolution(self, user_id: str) -> list:
        """The function returns value resolution of need iphone model for it user."""
        try:
            request = f"""SELECT val
                            FROM pixresolution JOIN iphone USING(id_pixresolution)
                            JOIN user USING(id_iphone)
                            WHERE user_id = {user_id}
                       """
            self.cursor.execute(request)
            return self.cursor.fetchall()

        except Exception:
            super_logger.error('Error get_iphone_info', exc_info=True)  


    def del_user(self, user_id: str) -> bool:
        """The function returns True if user was successfully deleted of DB else False."""
        try:
            request = f"""DELETE FROM user
                          WHERE user_id = {user_id}
                       """
            self.conn.execute(request)
            self.conn.commit()
            return True

        except Exception:
            super_logger.error('Error del_user', exc_info=True)
            return False


class Telegram:
    """The class for work with Telegram API."""
    def __init__(self):
        self.request_db = RequestsDb()
        self.hand_req_db = HandlerReqDb()

    def send_message(self, chat_id, text):
        """The function can send message necessary user."""
        try:
            method = "sendMessage"
            url = f"https://api.telegram.org/bot{token}/{method}"
            data = {"chat_id": chat_id, "text": text}
            requests.post(url, data=data)

        except Exception:
            super_logger.error('Error send_message', exc_info=True) 

    def select_iphone(self, user_id):
        """The function can call function for send buttons to
        user with all exists to DB of  iPhone model.

        """
        try:
            get_info = self.request_db.get_iphone_info()
            lst_iphones = self.hand_req_db.hand_iphone_info(get_info)
            self.button(lst_iphones, user_id)

        except Exception:
            super_logger.error('Error select_iphone', exc_info=True)

    def get_picture_chang_iph(self, user_id):
        """The function can call function for send buttons
        'Получить обои' and 'Изменить модель iphone'.

        """
        try:
            title_button = [[{"text": "Получить обои"}], [{"text": "Изменить модель iphone"}]]
            self.button(title_button, user_id)

        except Exception:
            super_logger.error('Error get_picture_chang_iph', exc_info=True)
    
    def get_start_butt(self, user_id):
        """The function can call function for send button 'Начать'."""
        try:
            title_button = [[{"text": "Начать"}]]
            self.button(title_button, user_id)

        except Exception:
            super_logger.error('Error get_picture_chang_iph', exc_info=True)

    def button(self, title_button: list, user_id: str):
        """The function can do request to telegram API for send buttons user."""
        try:
            method = "sendMessage"
            url = f"https://api.telegram.org/bot{token}/{method}"
            reply = json.dumps({"keyboard": title_button, "resize_keyboard": True})
            params = {"chat_id": user_id, "reply_markup": reply, "text": "👌"}
            a = requests.post(url, params)
            print(a.content)
        
        except Exception:
            super_logger.error('Error button', exc_info=True)

    def send_photo(self, chat_id: str):
        """The function can get photo of 'Picsum' API and send it to user."""
        try:
            all_pix = self.request_db.get_pixresolution(chat_id)
            if all_pix:
                ferst_pix = all_pix[0][0].split(' ')[0]
                second_pix = all_pix[0][0].split(' ')[1]
                method = "sendPhoto"
                url = f"https://api.telegram.org/bot{token}/{method}"
                url_foto = requests.get(f"https://picsum.photos/{ferst_pix}/{second_pix}").url
                data = {"chat_id": chat_id, "photo": url_foto}
                requests.post(url, data=data)

        except Exception:
            super_logger.error('Error send_photo', exc_info=True) 


class HandlerReqDb:
    """ """
    def __init__(self):
        self.connect_db = ConnectionDB().conn
        self.request_db = RequestsDb()

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

    def user_exist(self, user_id: str) -> bool:
        """ """
        try:
            user_info = self.request_db.get_user_info(user_id)
            if user_info:
                return True
            return False

        except Exception:
            super_logger.error('Error user_exist', exc_info=True)
            return False

    def get_iphone_list(self) -> list:
        """ """
        try:
            iphone_info = self.request_db.get_iphone_info()
            iphone_list = [i[0] for i in iphone_info]
            return iphone_list

        except Exception:
            super_logger.error('Error get_iphone_list', exc_info=True)

    def get_status_take_iphone(self, user_id: str) -> bool:
        """ """
        try:
            user_info = self.request_db.get_user_info(user_id)
            if user_info:
                status_take_iphone = user_info[0][3]
                if status_take_iphone:
                    return True
                return False

        except Exception:
            super_logger.error('Error get_status_take_iphone', exc_info=True)


class HandlerServer:
    """ """
    def __init__(self, request_json):
        self.request_db = RequestsDb()
        self.hand_req_db = HandlerReqDb()
        self.teleg = Telegram()
        self.req = request_json
        self.chat_id = self.req["message"]["chat"]["id"]
        self.text_message = self.req["message"]["text"] if "text" in self.req["message"] else ""

    def start_command(self):
        """ """
        user_exist = self.hand_req_db.user_exist(self.chat_id)
        if not user_exist:
            add_user = self.request_db.add_user_info(self.chat_id)
            if add_user:
                self.teleg.select_iphone(self.chat_id)
        else:
            status_take_iphone = self.hand_req_db.get_status_take_iphone(self.chat_id)
            if status_take_iphone:
                self.teleg.get_picture_chang_iph(self.chat_id)
            else:
                self.teleg.select_iphone(self.chat_id)

    def any_iphon_command(self):
        """ """
        user_exist = self.hand_req_db.user_exist(self.chat_id)
        if user_exist:
            stat_take_iphone = self.request_db.set_status_take_iphone(self.chat_id)
            set_id_iphone = self.request_db.set_id_iphone(self.chat_id, self.text_message)  # пользователю присваивается id_iphone
            if stat_take_iphone and set_id_iphone:
                self.teleg.get_picture_chang_iph(self.chat_id)

    def get_wallpapers_command(self):
        """ """
        user_exist = self.hand_req_db.user_exist(self.chat_id)
        stat_take_iphone = self.request_db.set_status_take_iphone(self.chat_id)
        if user_exist and stat_take_iphone:  # если пользователь есть в БД и он уже выбрал модель своего айфона
            self.teleg.send_message(self.chat_id, "Секундочку, Ваши обои тоже ждут встречи с Вами \U0001f929")
            self.teleg.send_photo(self.chat_id)

    def stop_command(self):
        """ """
        del_user = self.request_db.del_user(self.chat_id)
        if del_user:
            text = """Если Вы вновь захотите воспользоваться ботом, нажмите - "Начать" """
            self.teleg.get_start_butt(self.chat_id)
            self.teleg.send_message(self.chat_id, text)
            


    def select_comand(self):
        """ """
        if self.text_message == "/start":
            self.start_command()

        if self.text_message in self.hand_req_db.get_iphone_list():
            self.any_iphon_command()

        if self.text_message == "Получить обои":
            self.get_wallpapers_command()

        if self.text_message == "Изменить модель iphone":
            self.teleg.select_iphone(self.chat_id)

        if self.text_message == "Начать":
            self.start_command()

        if self.text_message == "/stop":
            self.stop_command()

