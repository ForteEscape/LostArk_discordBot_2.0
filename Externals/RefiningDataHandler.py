from Externals.DBhandler import DBhandler
from Externals.ExceptionHandler import ExceptionHandler


class RefiningDataHandler:
    def __init__(self):
        self.__db_connector = DBhandler()
        self.__db_conn = self.__db_connector.get_refining_data()
        self.__cursor = self.__db_connector.get_db_cursor()
        self.__exception_handler = ExceptionHandler("RefiningDataHandler").get_logger()

    def signup(self, uid, weapon_class, cur_step, cur_success_probability):
        try:
            sql = "insert into user_refining_data(" \
                  "user_id, weapon_class, cur_step, used_material_1, used_material_2, used_material_3," \
                  "used_material_4, used_gold, used_refining_helper_1, used_refining_helper_2, used_refining_helper_3,"\
                  "cur_ceiling_status, cur_success_prob, refining_count) " \
                  "value(%s, %s, %s, 0, 0, 0, 0, 0, 0, 0, 0, '0.0', %s, 0)"

            self.__cursor.execute(sql, [uid, weapon_class, cur_step, cur_success_probability])
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            self.__db_conn.commit()

    def update(self, datalist, uid):
        count, material_1, material_2, material_3, material_4, used_gold, refining_helper_1, refining_helper_2, \
        refining_helper_3, suc_prob, ceiling_status = datalist

        try:
            if ceiling_status == "-1" or suc_prob == "-1":
                sql = "update user_refining_data set used_material_1 = %s, used_material_2 = %s, used_material_3 = %s, " \
                      "used_material_4 = %s, used_gold = %s, used_refining_helper_1 = %s, used_refining_helper_2 = %s, " \
                      "used_refining_helper_3 = %s, refining_count = %s where user_id=%s"
                self.__cursor.execute(sql, [material_1, material_2, material_3, material_4, used_gold,
                                            refining_helper_1, refining_helper_2, refining_helper_3, count, uid])
            else:
                sql = "update user_refining_data set used_material_1 = %s, used_material_2 = %s, used_material_3 = %s, " \
                      "used_material_4 = %s, used_gold = %s, used_refining_helper_1 = %s, used_refining_helper_2 = %s, " \
                      "used_refining_helper_3 = %s, cur_ceiling_status = %s, cur_success_prob = %s, refining_count = %s " \
                      "where user_id=%s"

                self.__cursor.execute(sql, [material_1, material_2, material_3, material_4, used_gold,
                                            refining_helper_1, refining_helper_2, refining_helper_3,
                                            ceiling_status, suc_prob, count, uid])
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            self.__db_conn.commit()

    def data_transport(self, uid):
        """
        초기화 전에 기록한 데이터를 user_refining_record_data 테이블에 저장한다.
        :param uid: 유저 데이터를 찾기 위한 key
        """
        try:
            success_data = self.find_data(uid=uid)[0]
            sql = "insert into user_refining_record_data(" \
                  "user_id, weapon_class, success_step, used_material_1, used_material_2, used_material_3," \
                  "used_material_4, used_gold, used_refining_helper_1, used_refining_helper_2, used_refining_helper_3," \
                  "cur_ceiling_status, cur_success_prob, refining_count) " \
                  "value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.__cursor.execute(sql, [
                success_data["user_id"], success_data["weapon_class"], success_data["cur_step"],
                success_data["used_material_1"], success_data["used_material_2"], success_data["used_material_3"],
                success_data["used_material_4"], success_data["used_gold"], success_data["used_refining_helper_1"],
                success_data["used_refining_helper_2"], success_data["used_refining_helper_3"],
                success_data["cur_ceiling_status"], success_data["cur_success_prob"], success_data["refining_count"]
            ])
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            self.__db_conn.commit()

    def data_init(self, uid, s_prob):
        """
        강화 성공 시 현재 레벨 단계를 1 상승시키고 user_id, weapon_class, cur_step을 제외한 모든 데이터를 초기화한다.
        :param uid: 유저 데이터를 찾기 위한 key
        :param s_prob: 강화된 장비의 다음 단계 성공 확률
        """
        try:
            old_data = self.find_data(uid=uid)[0]
            sql = "update user_refining_data set cur_step = %s," \
                  "used_material_1 = %s, used_material_2 = %s, used_material_3 = %s, used_material_4 = %s, " \
                  "used_gold = %s, used_refining_helper_1 = %s, used_refining_helper_2 = %s, " \
                  "used_refining_helper_3 = %s, cur_ceiling_status = %s, cur_success_prob = %s ," \
                  "refining_count = %s where user_id=%s"

            self.__cursor.execute(sql, [old_data["cur_step"] + 1, 0, 0, 0, 0, 0, 0, 0, 0, '0.0', s_prob, 0, uid])
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            self.__db_conn.commit()

    def withdraw(self, uid):
        try:
            sql = "delete from user_refining_data where user_id=%s"
            self.__cursor.execute(sql, [uid])
            self.delete_record_data(uid=uid)
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            self.__db_conn.commit()

    def find_data(self, uid):
        try:
            sql = "select * from user_refining_data where user_id=%s"
            self.__cursor.execute(sql, [uid])

            result = self.__cursor.fetchall()
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            return result

    def find_record_data(self, uid):
        try:
            sql = "select * from user_refining_record_data where user_id=%s"
            self.__cursor.execute(sql, [uid])

            result = self.__cursor.fetchall()
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            return result

    def delete_record_data(self, uid):
        try:
            sql = "delete from user_refining_record_data " \
                  "where user_id in (select user_id from (select * from user_refining_record_data " \
                  "where user_id=%s) as resultTable)"

            self.__cursor.execute(sql, [uid])
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            self.__db_conn.commit()

