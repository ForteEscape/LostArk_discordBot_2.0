import csv
from Externals.ExceptionHandler import ExceptionHandler


class DataReader:
    def __init__(self):
        self.__data = None
        self.__raw_data = None
        self.__is_data_empty = True
        self.__exception_handler = ExceptionHandler("DataReader").get_logger()

    def read_csv(self, path):
        self.__is_data_empty = False

        try:
            with open(path, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                temp_list = []

                for row in csv_reader:
                    temp_list.append(row)

                self.__data = temp_list
        except UnicodeDecodeError:
            with open(path, 'r', encoding='cp949') as csvfile:
                csv_reader = csv.reader(csvfile)
                temp_list = []

                for row in csv_reader:
                    temp_list.append(row)

                self.__data = temp_list
        except Exception as e:
            self.__exception_handler.debug(e)

    def read_txt(self, path):
        self.__is_data_empty = False

        try:
            with open(path, 'r', encoding='utf-8') as txtfile:
                txt_reader = txtfile.read()
                self.__raw_data = txt_reader
                temp_list = []

                for row in txt_reader:
                    temp_list.append(row.strip())

                self.__data = temp_list
        except UnicodeDecodeError:
            with open(path, 'r', encoding='cp949') as txtfile:
                txt_reader = txtfile.read()
                self.__raw_data = txt_reader
                temp_list = []

                for row in txt_reader:
                    temp_list.append(row.strip())

                self.__data = temp_list
        except Exception as e:
            self.__exception_handler.debug(e)

    def clean_data(self, path):
        self.__data = None
        self.__is_data_empty = True

    def get_data_status(self):
        return self.__is_data_empty

    def get_data(self):
        return self.__data

    def get_raw_data(self):
        return self.__raw_data
