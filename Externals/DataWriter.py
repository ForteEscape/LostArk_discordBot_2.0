import csv
from Externals.ExceptionHandler import ExceptionHandler


class DataWriter:
    def __init__(self):
        self.__write_status = False
        self.__exception_handler = ExceptionHandler("DataWriter")

    def write_text(self, path, data):
        try:
            with open(path, 'w', newline='') as text_file:
                text_file.write(data)
        except Exception as e:
            self.__exception_handler.print_error(e)
            self.__write_status = False
            return
        else:
            self.__write_status = True
            return

    def write_csv(self, path, data):
        try:
            with open(path, 'w', newline='') as csv_file:
                csv_file = csv.writer(csv_file)
                csv_file.writerows(data)
        except Exception as e:
            self.__exception_handler.print_error(e)
            self.__write_status = False
            return
        else:
            self.__write_status = True
            return

    def get_write_status(self):
        return self.__write_status

