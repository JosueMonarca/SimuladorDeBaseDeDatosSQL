import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.service.dbms_service import DBMS
from src.app import exceptions


class TestCRUDOperations(unittest.TestCase):

    def setUp(self):
        self.dbms = DBMS()
        self.db_name = "test_db_crud"
        self.dbms.create_database(self.db_name)
        self.dbms.use_database(self.db_name)
        self.dbms.create_table("users", ["id INT", "name TEXT"])

    def tearDown(self):
        DataBase._instances = {}

    def test_insert_single_record(self):
        self.dbms.insert("users", ["1", "Juan"])
        self.assertEqual(len(self.dbms.current_db.tables["users"].records), 1) # type: ignore

    def test_insert_multiple_records(self):
        self.dbms.insert("users", ["1", "Juan"])
        self.dbms.insert("users", ["2", "Maria"])
        self.assertEqual(len(self.dbms.current_db.tables["users"].records), 2) # type: ignore

    def test_insert_into_nonexistent_table(self):
        with self.assertRaises(exceptions.TableNotFoundError):
            self.dbms.insert("nonexistent", ["1", "Juan"])

    def test_select_all(self):
        self.dbms.insert("users", ["1", "Juan"])
        self.dbms.insert("users", ["2", "Maria"])
        result = self.dbms.select("users")
        self.assertEqual(len(result), 2)

    def test_select_with_where(self):
        self.dbms.insert("users", ["1", "Juan"])
        self.dbms.insert("users", ["2", "Maria"])
        result = self.dbms.select("users", where_clause={"column": "id", "operator": "=", "value": 1})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)

    def test_select_nonexistent_table(self):
        with self.assertRaises(exceptions.TableNotFoundError):
            self.dbms.select("nonexistent")

    def test_update_with_where(self):
        self.dbms.insert("users", ["1", "Juan"])
        self.dbms.insert("users", ["2", "Maria"])
        count = self.dbms.update("users", {"column": "name", "value": "Pedro"}, {"column": "id", "operator": "=", "value": 1})
        self.assertGreater(count, 0)
        self.assertEqual(self.dbms.current_db.tables["users"].records[0][1], "Pedro") # type: ignore

    def test_update_without_where(self):
        self.dbms.insert("users", ["1", "Juan"])
        self.dbms.insert("users", ["2", "Maria"])
        count = self.dbms.update("users", {"column": "name", "value": "Unknown"}, None)
        self.assertEqual(count, 2)

    def test_delete_with_where(self):
        self.dbms.insert("users", ["1", "Juan"])
        self.dbms.insert("users", ["2", "Maria"])
        count = self.dbms.delete("users", {"column": "id", "operator": "=", "value": 1})
        self.assertGreater(count, 0)
        self.assertEqual(len(self.dbms.current_db.tables["users"].records), 1) # type: ignore

    def test_delete_all(self):
        self.dbms.insert("users", ["1", "Juan"])
        self.dbms.insert("users", ["2", "Maria"])
        count = self.dbms.delete("users", None)
        self.assertEqual(count, 2)
        self.assertEqual(len(self.dbms.current_db.tables["users"].records), 0) # type: ignore


if __name__ == '__main__':
    unittest.main()