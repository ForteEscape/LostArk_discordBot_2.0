from Externals.DBhandler import DBhandler
from Externals.ExceptionHandler import ExceptionHandler


class RefiningDataHandler:
    def __init__(self):
        self.__db_connector = DBhandler()
        self.__db_conn = self.__db_connector.get_refining_data()
        self.__cursor = self.__db_connector.get_db_cursor()
        self.__exception_handler = ExceptionHandler("RefiningDataHandler").get_logger()

    def ready_signup(self, uid):
        try:
            sql = "select * from user_refining_data where user_id=%s"
            self.__cursor.execute(sql, [uid])
            find_user = self.__cursor.fetchall()

            if not find_user:
                return False
            else:
                return True

        except Exception as e:
            self.__exception_handler.debug(e)

    def signup(self, uid, weapon_class):
        try:
            sql = "insert into user_refining_data(user_id, weapon_class) value(%s, %s)"
            self.__cursor.execute(sql, [uid, weapon_class])
            self.__db_conn.commit()
        except Exception as e:
            self.__exception_handler.debug(e)

    def withdraw(self, uid):
        try:
            sql = "delete from user_refining_data where user_id=%s"
            self.__cursor.execute(sql, [uid])
            self.__db_conn.commit()
        except Exception as e:
            self.__exception_handler.debug(e)

