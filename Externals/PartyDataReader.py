import csv
from Externals.DataReader import DataReader


class PartyDataReader(DataReader):
    """
    DataReader를 상속받아 파티 데이터 처리를 위한 전용 클래스
    PartyHandler 에게 데이터를 제공해주는 역할을 함
    """
    def __init__(self):
        super().__init__()
        self.__party_data_raw = None
        self.party_name_list = []
        self.output_list = []
        self.week_list = []
        self.__member_id = None

    def read_txt(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = file.read().splitlines()
            file.close()
            reader.append('')
        except UnicodeDecodeError:
            with open(path, 'r', encoding='cp949') as file:
                reader = file.read().splitlines()
            file.close()
            reader.append('')

        self.__party_data_raw = reader

    def read_csv(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as member_id_file:
                file_reader = csv.reader(member_id_file)
        except UnicodeDecodeError:
            with open(path, 'r', encoding='cp949') as member_id_file:
                file_reader = csv.reader(member_id_file)

        self.__member_id = list(file_reader)

    def get_raw_party_data(self):
        return self.__party_data_raw

    def get_member_id(self):
        return self.__member_id
