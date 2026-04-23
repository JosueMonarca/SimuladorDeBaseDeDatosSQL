import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.service.dbms_service import DBMS
from src.app import exceptions


class TestQueryProcessor(unittest.TestCase):

    def setUp(self):
        self.dbms = DBMS()
        DataBase._instances = {}

    def tearDown(self):
        DataBase._instances = {}

    def test_create_database_success(self):
        self.dbms.create_database("test_db_create")
        self.assertTrue(DataBase.exists("test_db_create"))

    def test_create_duplicate_database(self):
        self.dbms.create_database("test_db")
        with self.assertRaises(exceptions.DatabaseAlreadyExistsError):
            self.dbms.create_database("test_db")

    def test_drop_database_success(self):
        self.dbms.create_database("test_db_drop")
        self.dbms.drop_database("test_db_drop")
        self.assertFalse(DataBase.exists("test_db_drop"))

    def test_drop_nonexistent_database(self):
        with self.assertRaises(exceptions.DatabaseNotFoundError):
            self.dbms.drop_database("nonexistent_db")


if __name__ == '__main__':
    unittest.main()