from Src.Logics.storage_prototype import storage_prototype
from Src.Logics.start_factory import start_factory
import unittest
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from datetime import datetime

class prototype_test(unittest.TestCase):
    def test_filter(self):

        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
        data = start.storage.data[key]

        start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        stop_date = datetime.strptime("2024-01-10", "%Y-%m-%d")
        prototype = storage_prototype(data)

        result1 = prototype.filter(start_date, stop_date)
        stop_date = datetime.strptime("2024-01-05", "%Y-%m-%d")
        result2 = result1.filter(start_date, stop_date)

        self.assertIsInstance(result1, storage_prototype)
        self.assertTrue(prototype.is_empty)

    def test_filter(self):

        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        nomenclatures = start.create_nomenclatures()
        nomenclature_id = nomenclatures[0].id

        prototype = storage_prototype(start.storage.data)
        result = prototype.filter(nomenclature_id)

        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item) for item in result))


    def test_filter_receipt(self):

        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
        data = list(start.storage.data.values())

        receipt_id = "TestReceiptID"
        prototype = storage_prototype(data)

        result = prototype.filter_receipt(receipt_id)

        self.assertIsInstance(result, list)