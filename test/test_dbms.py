import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.service.dbms_service import DBMS
from src.app.controller.database import DataBase


class TestDBMS(unittest.TestCase):

    def setUp(self):
        self.dbms = DBMS()
        DataBase._instances = {}

    def tearDown(self):
        DataBase._instances = {}

    def test_create_database(self):
        self.dbms.create_database("test_db")
        self.assertTrue(DataBase.exists("test_db"))

    def test_use_database(self):
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.assertIsNotNone(self.dbms.current_db)

    def test_create_table(self):
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.dbms.create_table("users", ["id INT", "name TEXT"])

    def test_insert(self):
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.dbms.create_table("users", ["id INT", "name TEXT"])
        self.dbms.insert("users", ["1", "Juan"])

    def test_select(self):
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.dbms.create_table("users", ["id INT", "name TEXT"])
        self.dbms.insert("users", ["1", "Juan"])
        result = self.dbms.select("users")
        self.assertEqual(len(result), 1)

    def test_select_with_where(self):
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.dbms.create_table("users", ["id INT", "name TEXT"])
        self.dbms.insert("users", ["1", "Juan"])
        self.dbms.insert("users", ["2", "Maria"])
        result = self.dbms.select("users", where_clause={"column": "id", "operator": "=", "value": 1})
        self.assertEqual(len(result), 1)

    def test_update(self):
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.dbms.create_table("users", ["id INT", "name TEXT"])
        self.dbms.insert("users", ["1", "Juan"])
        count = self.dbms.update("users", {"column": "name", "value": "Pedro"}, {"column": "id", "operator": "=", "value": 1})
        self.assertGreater(count, 0)

    def test_delete(self):
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.dbms.create_table("users", ["id INT", "name TEXT"])
        self.dbms.insert("users", ["1", "Juan"])
        count = self.dbms.delete("users", {"column": "id", "operator": "=", "value": 1})
        self.assertGreater(count, 0)

    def test_drop_table(self):
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.dbms.create_table("users", ["id INT"])
        self.dbms.drop_table("users")
        self.assertFalse(self.dbms.current_db.exist_table("users")) # type: ignore

    def test_show_databases(self):
        self.dbms.create_database("db1")
        self.dbms.create_database("db2")
        result = self.dbms.list_databases()
        self.assertEqual(len(result), 2)

    def test_show_tables(self):
        self.dbms.create_database("test_db")
        self.dbms.use_database("test_db")
        self.dbms.create_table("users", ["id INT"])
        result = self.dbms.list_tables()
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()