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
                            id_pixresolution INTEGER,
                            val TEXT NOT NULL,
                            UNIQUE(val)
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
                            ON DELETE CASCADE
                            )"""
                self.connect_db.execute(request)
                self.connect_db.commit()
        except Exception:
            super_logger.error('Error create_user', exc_info=True)

    def add_pixresolution(self):
        """This method fills in the 'pixresolution' table."""
        try:
            with self.connect_db:
                request = """INSERT INTO pixresolution(id_pixresolution, val)
                             VALUES(1, '750 1334'),
                                   (2, '1080 1920'),
                                   (3, '640 1136'),
                                   (4, '1125 2436'),
                                   (5, '1242 2688'),
                                   (6, '828 1792')
                          """
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error add_pixresolution', exc_info=True)

    def add_iphone(self):
        """This method fills in the 'iphone' table."""
        try:
            with self.connect_db:
                request = """INSERT INTO iphone(title, id_pixresolution)
                             VALUES(iPhone 6, 1),
                                   (iPhone 6+, 1),
                                   (iPhone 6S, 1),
                                   (iPhone 6S+, 2),
                                   (iPhone SE, 3),
                                   (iPhone 7, 1),
                                   (iPhone 7+, 1),
                                   (iPhone 8, 1),
                                   (iPhone 8+, 2),
                                   (iPhone X, 4),
                                   (iPhone XS, 4),
                                   (iPhone XS Max, 5),
                                   (iPhone XR, 6),
                                   (iPhone 11, 6),
                                   (iPhone 11 Pro, 4),
                                   (iPhone 11 Pro Max, 5),

                          """
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error add_iphone', exc_info=True)


def main():
    db = PreparDb()
    # db.create_pixresolution()
    # db.create_iphone()
    # db.create_user()
    db.add_pixresolution()
    # add_iphone

if __name__ == "__main__":
    main()
