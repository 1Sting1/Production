from Src.Logics.convert_factory import convert_factory
from Src.Logics.process_factory import process_factory
from Src.Logics.storage_prototype import storage_prototype
from Src.exceptions import argument_exception, exception_proxy
from datetime import datetime
import json

class storage_service:
    __data = []
    
    def __init__(self, data: list) -> None:
        if len(data) == 0:
            raise argument_exception("Некорректно переданы параметры!")
        
        self.__data = data
        self.__convert = convert_factory()
        
        
    def create_turns(self, start_period: datetime, stop_period:datetime ) -> dict:

        if not isinstance(start_period, datetime) or not isinstance(stop_period, datetime):
            raise argument_exception("Некорректно переданы параметры!")

        exception_proxy.validate(start_period, datetime)
        exception_proxy.validate(stop_period, datetime)
        
        if start_period > stop_period:
            raise argument_exception("Некорректно переданы параметры!")
        
        # Фильтруем      
        prototype = storage_prototype(  self.__data )  
        filter = prototype.filter( start_period, stop_period)
            
        # Подобрать процессинг    
        key_turn = process_factory.turn_key()
        processing = process_factory().create( key_turn  )
    
        # Обороты
        turns =  processing().process( filter.data )
        return turns

    def get_turns(self, nomenclature_id: str) -> dict:
        if not isinstance(nomenclature_id, str):
            raise argument_exception("Некорректно переданы параметры!")

        prototype = storage_prototype(self.__data)

        filtred_data = prototype.filter(nomenclature_id)

        key_turn = process_factory.turn_key()
        processing = process_factory().create(key_turn)

        turns = processing().process(filtred_data.data)
        return turns


    def get_debit_rec(self, receipt_row: str, storage: str) -> list:
        if not isinstance(receipt_row, str) or not isinstance(storage, str):
            raise argument_exception("Некорректно переданы параметры!")

        prototype = storage_prototype(self.__data)
        filtred_data = prototype.filter(receipt_row)

        debits = self.generate_debit(filtred_data, storage)

        return debits


    def generate_debit(self, filtred_data, storage):
        debits = []
        for transaction in filtred_data.data:
            if transaction.storage == storage and not transaction.storage_type:
                debit_transaction = {
                    'nomenclature': transaction.nomenclature,
                    'storage': transaction.storage,
                    'unit': transaction.unit,
                    'value': -transaction.value
                }
                debits.append(debit_transaction)
        return debits

    @staticmethod
    def create_response( data: list, app):
        """"
            Сформировать данные для сервера
        """
        if app is None:
            raise argument_exception("Некорректно переданы параметры!")

        # Преоброзование
        data = convert_factory().serialize( data )
        json_text = json.dumps( data, sort_keys = True, indent = 4,  ensure_ascii = False)  
   
        # Подготовить ответ    
        result = app.response_class(
            response = f"{json_text}",
            status = 200,
            mimetype = "application/json; charset=utf-8"
        )
        
        return result