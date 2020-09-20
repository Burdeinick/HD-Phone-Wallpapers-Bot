import sys
import sqlite3
sys.path.insert(0, 'Application')
from scripts.logic.logic import ConnectionDB
from logger.log import MyLogging


super_logger = MyLogging().setup_logger('preparing_db_logger',
                                        'Application/logger/logfile.log')


class DropTableDb:
    """The class for deleting tables."""
    def __init__(self):
        self.connect_db = ConnectionDB().conn

    def drop_pixresolution(self):
        """Request to drop the 'pixresolution' table."""
        try:
            with self.connect_db:
                request = """DROP TABLE IF EXISTS pixresolution"""
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error drop_pixresolution', exc_info=True)

    def drop_iphone(self):
        """Request to drop the 'iphone' table."""
        try:
            with self.connect_db:
                request = """DROP TABLE IF EXISTS iphone"""
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error drop_iphone', exc_info=True)

    def drop_user(self):
        """Request to drop the 'user' table."""
        try:
            with self.connect_db:
                request = """DROP TABLE IF EXISTS user"""
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error drop_user', exc_info=True)


def main():
    db = DropTableDb()
    db.drop_pixresolution()
    db.drop_iphone()
    db.drop_user()


if __name__ == "__main__":
    main()
