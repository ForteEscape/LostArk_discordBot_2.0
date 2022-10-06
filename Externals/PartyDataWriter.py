from Externals.DataWriter import DataWriter
from Externals.ExceptionHandler import ExceptionHandler


class PartyDataWriter(DataWriter):
    def __init__(self):
        super(PartyDataWriter, self).__init__()
        self.__filename_list = []
        self.__exception_handler = ExceptionHandler("PartyDataWriter").get_logger()

    def write_party_text(self, path, data):
        try:
            datalist = []
            for element in data:
                # EOF
                if element == '':
                    filename = datalist[0]
                    self.__filename_list.append(filename)
                    self.write_text(path + filename + '.txt', datalist)
                    datalist.clear()
                else:
                    datalist.append(element)
        except Exception as e:
            self.__exception_handler.debug(e)

    def write_text(self, path, datalist):
        try:
            with open(path, 'w', newline='') as file:
                file.writelines('\n'.join(datalist))
        except Exception as e:
            self.__exception_handler.debug(e)

    def get_party_name_list(self):
        return self.__filename_list
