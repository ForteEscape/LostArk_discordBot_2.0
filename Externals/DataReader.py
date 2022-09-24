import csv


class DataReader:
    def __init__(self):
        self.__data = None
        self.__is_data_empty = True

    def read_csv(self, path):
        self.__is_data_empty = False

        with open(path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            temp_list = []

            for row in csv_reader:
                temp_list.append(row)

            self.__data = temp_list

    def read_txt(self, path):
        self.__is_data_empty = False

        with open(path, 'r', encoding='utf-8') as txtfile:
            txt_reader = txtfile.readline()
            temp_list = []

            for row in txt_reader:
                temp_list.append(row.strip())

            self.__data = temp_list

    def clean_data(self, path):
        self.__data = None
        self.__is_data_empty = True

    def get_data_status(self):
        return self.__is_data_empty

    def get_data(self):
        return self.__data
