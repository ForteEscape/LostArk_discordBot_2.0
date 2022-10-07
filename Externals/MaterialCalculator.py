from Externals.ExceptionHandler import ExceptionHandler
import decimal


"""
장비 강화 시도 시 숨결, 소모 재료, 골드, 장인의 기운, 성공 확률을 업데이트한다.
성공 확률은 원래 트라이의 10%를 가산하여 계산한다. 단, 원래 성공 확률의 2배를 초과하면 안된다.
장인의 기운은 현재 실행하는 확률의 46.5%를 가산하여 계산한다. 단, 계산 후 100%가 초과 시 100%로 고정된다.
장인의 기운은 계산값의 소수점 셋째 자리에서 반올림하여 계산한다.
"""


class MaterialCalculator:
    def __init__(self):
        self.__datalist = []
        self.__exception_handler = ExceptionHandler("MaterialCalculator").get_logger()

    def calculate_material(self, datalist, is_success, used_helper, db_data_dic):
        material_1, material_2, material_3, material_4, used_gold, refining_helper_1, refining_helper_2, refining_helper_3, suc_prob = datalist

        try:
            self.__datalist.append(db_data_dic["refining_count"] + 1)
            self.__datalist.append(db_data_dic["used_material_1"] + material_1)
            self.__datalist.append(db_data_dic["used_material_2"] + material_2)
            self.__datalist.append(db_data_dic["used_material_3"] + material_3)
            self.__datalist.append(db_data_dic["used_material_4"] + material_4)
            self.__datalist.append(db_data_dic["used_gold"] + used_gold)

            if used_helper:
                self.__datalist.append(db_data_dic["used_refining_helper_1"] + refining_helper_1)
                self.__datalist.append(db_data_dic["used_refining_helper_2"] + refining_helper_2)
                self.__datalist.append(db_data_dic["used_refining_helper_3"] + refining_helper_3)
            else:
                self.__datalist.append(db_data_dic["used_refining_helper_1"])
                self.__datalist.append(db_data_dic["used_refining_helper_2"])
                self.__datalist.append(db_data_dic["used_refining_helper_3"])

            if not is_success:
                # 강화 성공 확률 상승
                success_prob = round(float(db_data_dic["cur_success_prob"]) + (float(suc_prob) * 0.1), 2)

                if success_prob > suc_prob * 2:
                    success_prob = float(db_data_dic["cur_success_prob"])

                self.__datalist.append(str(success_prob))

                # 장인의 기운 상승
                context = decimal.getcontext()
                context.rounding = decimal.ROUND_HALF_UP
                current_try_prob = float(db_data_dic["cur_success_prob"])
                if used_helper:
                    if db_data_dic["cur_step"] + 1 >= 24:
                        current_try_prob += 1
                    else:
                        current_try_prob += suc_prob

                ceiling_status = round(decimal.Decimal(db_data_dic["cur_ceiling_status"]) +
                                       round(decimal.Decimal(str(current_try_prob * 0.465)), 2), 2)
                if ceiling_status >= 100.0:
                    ceiling_status = 100.0

                self.__datalist.append(str(ceiling_status))
            else:
                # 성공 시 쌓이는 기운과 쌓이는 확률은 의미가 없음
                self.__datalist.append("-1")
                self.__datalist.append("-1")
        except Exception as e:
            self.__exception_handler.debug(e)

    def list_clear(self):
        self.__datalist.clear()

    def get_datalist(self):
        return self.__datalist

