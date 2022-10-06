from Externals.PartyDataReader import PartyDataReader
from Externals.ExceptionHandler import ExceptionHandler
from Externals.DataTable import DataTable

"""
기존 make_party_data_output 메서드를 객체화

기존 메서드는 아래 구조로 진행된다.
1. 만들어진 각 파티 이름을 가진 party_list.txt를 읽는다.
2. 읽은 파티 이름을 사용하여 파일을 찾고 해당 파티 파일 데이터를 읽는다.
3. 파티 이름을 이용하여 파티의 출발 시간을 계산하고, 참가 인원을 계산한다.
4. prettytable 객체를 만들어 파티의 구조를 만들고 여러 정보와 함께 리스트에 넣는다.
4-1. 리스트 원소의 구조는 다음과 같다.
    [(출발 파티의)파일이름, 파티 구조 객체, 출발 요일, 출발 시간, 참가 인원 리스트]

해당 클래스는 최종 결과물인 리스트를 가지고 있으며 호출받을 시 해당 리스트 데이터를 넘겨준다.
"""


class PartyData:
    def __init__(self):
        self.__output_list = []
        self.__week_list = []
        self.__data_status = False
        self.__party_data_reader = PartyDataReader()
        self.__party_table = DataTable()
        self.__exception_handler = ExceptionHandler("PartyData").get_logger()

    def make_output_data(self):
        try:
            path_party_list = './data/party_data/party_list.txt'
            party_data_prefix = './data/party_data/'

            self.__party_data_reader.read_txt(path_party_list)

            raw_data = self.__party_data_reader.get_raw_party_data()
            raw_data.pop()

            for filename in raw_data:
                self.__party_data_reader.read_txt(party_data_prefix + filename + ".txt")
                party_data = self.__party_data_reader.get_raw_party_data()
                party_data.pop()

                party_info_list = filename.split()
                day_of_week = party_info_list[0]

                time = party_info_list[2]
                time = time.replace('시', ' ')
                time = time.replace('분', '')
                participated_member_list = []

                for index in range(1, 5):
                    member_list = party_data[index].split()
                    participated_member_list.append(member_list[0])
                    participated_member_list.append(member_list[1])

                self.__week_list.append(day_of_week)

                self.__party_table.make_table(party_data)
                party_table = self.__party_table.get_data_table()

                self.__output_list.append([filename, party_table, day_of_week, time, participated_member_list])
        except Exception as e:
            self.__exception_handler.debug(e)

    def clear_data(self):
        self.__output_list.clear()
        self.__week_list.clear()

    def get_output_list(self):
        return self.__output_list

    def get_week_list(self):
        return self.__week_list

