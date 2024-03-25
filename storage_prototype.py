from Src.Models.nomenclature_model import nomenclature_model
from Src.errors import error_proxy
from datetime import datetime

class storage_prototype(error_proxy):
    __data = []

    def __init__(self, data: list) -> None:
        if len(data) <= 0:
            self.error = "Некорректно переданы параметры!"

        self.__data = data

    def filter(self, start_period: datetime, stop_period: datetime):
        def date_filter(self, start_period: datetime, stop_period: datetime):
            """
                Отфильтровать по периоду
            Args:
                data (list): список складских транзакций
                start_period (datetime): начало
                stop_period (datetime): окончание
            Returns:
                storage_prototype: _description_
            """
            if len(self.__data) <= 0:
                self.error = "Некорректно переданы параметры!"

            if start_period > stop_period:
                self.error = "Некорректный период!"

            if not self.is_empty:
                return self.__data

            result = []
            for item in self.__data:
                if item.period > start_period and item.period <= stop_period:
                    result.append(item)

            return storage_prototype(result)

    def nomenclature_filter(self, nomenclature: nomenclature_model):
        if not isinstance(nomenclature, nomenclature_model):
            self.error = "Некорректная номенклатура!"
        if not self.is_empty:
            return self.__data

        result = []
        for item in self.__data:
            if item.nomenclature.id == nomenclature.id:
                result.append(item)

        return storage_prototype(result)

    @property
    def data(self):
        return self.__data
                
                   
            
            
        
    