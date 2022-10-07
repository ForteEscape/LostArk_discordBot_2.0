from Externals.ExceptionHandler import ExceptionHandler
import pandas as pd


class RefiningMaterialData:
    def __init__(self):
        self.__material_dataframe_list = []
        self.__material_class_list = ["low.csv", "middle.csv", "high.csv"]
        self.__exception_handler = ExceptionHandler("RefiningMaterialData").get_logger()

        self.__read_data()

    def __read_data(self):
        path_prefix = "./data/refining_data/weapon_material_"

        for i in range(3):
            try:
                material_data = pd.read_csv(path_prefix + self.__material_class_list[i], encoding='utf-8')
            except UnicodeDecodeError:
                material_data = pd.read_csv(path_prefix + self.__material_class_list[i], encoding='cp949')
                material_data.set_index("목표단계", inplace=True)
                self.__material_dataframe_list.append(material_data)
            except Exception as e:
                self.__exception_handler.debug(e)
            else:
                material_data.set_index("목표단계", inplace=True)
                self.__material_dataframe_list.append(material_data)

    def get_data(self, target):
        data_frame = None

        if target == "유물":
            data_frame = self.__material_dataframe_list[0]
        elif target == "상위유물":
            data_frame = self.__material_dataframe_list[1]
        elif target == "상위고대":
            data_frame = self.__material_dataframe_list[2]

        return data_frame
