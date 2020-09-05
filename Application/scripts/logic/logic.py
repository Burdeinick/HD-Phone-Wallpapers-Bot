import json
import sqlite3
import requests
import sys
sys.path.insert(0, 'Application')
from logger.log import MyLogging



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

    def add_user_id(self, user_id: str) -> bool:
        """ """
        try:
            request = f"""INSERT INTO user(id_user)
                          VALUES({user_id})
                       """
            self.conn.execute(request)
            self.conn.commit()
            return True

        except Exception:
            super_logger.error('Error', exc_info=True)
            return False


class Telegram:
    """ """
    def __init__(self):
        self.cookies = dict()

    def send_message(self, chat_id, text):
        method = "sendMessage"
        token = ""
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)

