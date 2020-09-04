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


def main():
    db = PreparDb()


if __name__ == "__main__":
    main()
