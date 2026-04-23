import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.service.dbms_service import DBMS
from src.app.controller.database import DataBase


class TestTransactionIntegration(unittest.TestCase):

    def setUp(self):
        self.dbms = DBMS()
        DataBase._instances = {}
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.dbms.create_table("users", ["id INT", "name TEXT"])
        self.dbms.insert("users", ["1", "Juan"])

    def tearDown(self):
        DataBase._instances = {}

    def test_begin_transaction(self):
        self.dbms.begin_transaction()
        self.assertTrue(self.dbms.is_in_transaction())

    def test_commit_transaction(self):
        self.dbms.begin_transaction()
        self.dbms.insert("users", ["2", "Maria"])
        self.dbms.commit_transaction()
        self.assertEqual(len(self.dbms.current_db.tables["users"].records), 2) # type: ignore

    def test_rollback_transaction(self):
        self.dbms.begin_transaction()
        self.dbms.insert("users", ["2", "Maria"])
        self.dbms.rollback_transaction()
        self.assertEqual(len(self.dbms.current_db.tables["users"].records), 1) # type: ignore

    def test_rollback_restores_original_data(self):
        self.dbms.begin_transaction()
        self.dbms.update("users", {"column": "name", "value": "Pedro"}, {"column": "id", "operator": "=", "value": 1})
        self.dbms.rollback_transaction()
        self.assertEqual(self.dbms.current_db.tables["users"].records[0][1], "Juan") # type: ignore

    def test_begin_without_db(self):
        dbms2 = DBMS()
        with self.assertRaises(Exception):
            dbms2.begin_transaction()


if __name__ == '__main__':
    unittest.main()