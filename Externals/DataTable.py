from prettytable import PrettyTable
from Externals.ExceptionHandler import ExceptionHandler

"""
prettytable 라이브러리를 이용하여 파티 인원 구조를 생성
DataTable은 이 파티 인원 구조를 가지고 있다가 요청이 올 시 해당 데이터를 반환
"""


class DataTable:
    def __init__(self):
        self.__data_table = None
        self.__exception_handler = ExceptionHandler("DataTable").get_logger()

    def make_table(self, data):
        table = PrettyTable()

        try:
            table.field_names = ["1파티", "2파티"]

            for index in range(1, 5):
                member_list = data[index].split()
                table.add_row(member_list)
        except Exception as e:
            self.__exception_handler.debug(e)
            return

        self.__data_table = table

    def get_data_table(self):
        return self.__data_table
