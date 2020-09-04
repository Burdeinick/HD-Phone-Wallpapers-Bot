import sys
import sqlite3
sys.path.insert(0, 'Application')
from scripts.logic.logic import ConnectionDB
from logger.log import MyLogging


super_logger = MyLogging().setup_logger('preparing_db_logger',
                                        'Application/logger/logfile_preparing.log')


class PreparDb:
    """The class for creating tables in a database."""
    def __init__(self):
        self.connect_db = ConnectionDB().conn

    def foreign_keys_on(self):
        """Allows you to use linked keys."""
        try:
            with self.connect_db:
                request = """PRAGMA foreign_keys=on"""
                self.connect_db.execute(request)
        except Exception:
            super_logger.error('Error foreign_keys_on', exc_info=True)

    def create_pixresolution(self):
        """This method creates the 'pixresolution' table."""
        try:
            with self.connect_db:
                request = """CREATE TABLE IF NOT EXISTS pixresolution(
                            id_pixresolution INTEGER PRIMARY KEY
                            AUTOINCREMENT NOT NULL,
                            val TEXT NOT NULL,
                            
                            )"""
                self.connect_db.execute(request)
                self.connect_db.commit()
        except Exception:
            super_logger.error('Error create_pixresolution', exc_info=True)       

    def create_iphone(self):
        """This method creates the 'iphone' table."""
        try:
            with self.connect_db:
                request = """CREATE TABLE IF NOT EXISTS iphone(
                            id_iphone INTEGER PRIMARY KEY
                            AUTOINCREMENT NOT NULL,

                            title TEXT NOT NULL,
                            id_pixresolution INTEGER NOT NULL,
                            FOREIGN KEY (id_pixresolution)
                            REFERENCES pixresolution(id_pixresolution)
                            ON DELETE CASCADE,
                            UNIQUE(title)
                            )"""
                self.connect_db.execute(request)
                self.connect_db.commit()
        except Exception:
            super_logger.error('Error create_iphone', exc_info=True) 

    def create_user(self):
        """This method creates the 'user' table."""
        try:
            with self.connect_db:
                request = """CREATE TABLE IF NOT EXISTS user(
                            id_db_user INTEGER PRIMARY KEY
                            AUTOINCREMENT NOT NULL,groups
                            id_user TEXT NOT NULL,
                            id_iphone INTEGER NOT NULL,
                            FOREIGN KEY (id_iphone)
                            REFERENCES iphone(id_iphone)
                            ON DELETE CASCADE,
                            )"""
                self.connect_db.execute(request)
                self.connect_db.commit()
        except Exception:
            super_logger.error('Error create_user', exc_info=True)

def main():
    db = PreparDb()


if __name__ == "__main__":
    main()
