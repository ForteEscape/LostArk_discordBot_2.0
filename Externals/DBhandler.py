import pymysql
from Externals.ExceptionHandler import ExceptionHandler


class DBhandler:
    def __init__(self):
        self.__user_refining_data = None
        self.__exception_handler = ExceptionHandler("DB_handler").get_logger()

        self.set_db()

    def set_db(self):
        try:
            self.__user_refining_data = pymysql.connect(
                user='root',
                passwd='0000',
                host='localhost',
                db='refining_db',
                charset='utf8'
            )
        except Exception as e:
            self.__exception_handler.debug(e)

    def get_db_cursor(self):
        cursor = self.__user_refining_data.cursor(pymysql.cursors.DictCursor)
        return cursor

    def get_refining_data(self):
        return self.__user_refining_data
