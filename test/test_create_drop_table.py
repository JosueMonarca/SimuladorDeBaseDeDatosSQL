import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.query_processor.CREATE_TABLE import create_table
from src.app.query_processor.DROP_TABLE import drop_table


class TestCreateTable(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_table"
        DataBase.get_instance(self.db_name)
        self.db = DataBase.get_instance(self.db_name)

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_create_table_success(self):
        success, msg = create_table(self.db_name, "users", ["id INT", "name TEXT"])
        self.assertTrue(success)
        self.assertTrue(self.db.exist_table("users"))

    def test_create_table_with_columns(self):
        create_table(self.db_name, "products", ["id INT", "name TEXT", "price FLOAT"])
        table = self.db.tables["products"]
        self.assertEqual(len(table.metadata.columns), 3)

    def test_create_duplicate_table(self):
        create_table(self.db_name, "users", ["id INT"])
        success, msg = create_table(self.db_name, "users", ["id INT"])
        self.assertFalse(success)
        self.assertIn("already exists", msg)


class TestDropTable(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_drop_table"
        DataBase.get_instance(self.db_name)
        self.db = DataBase.get_instance(self.db_name)
        create_table(self.db_name, "users", ["id INT"])

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_drop_table_success(self):
        success, msg = drop_table(self.db_name, "users")
        self.assertTrue(success)
        self.assertFalse(self.db.exist_table("users"))

    def test_drop_nonexistent_table(self):
        success, msg = drop_table(self.db_name, "nonexistent")
        self.assertFalse(success)
        self.assertIn("does not exist", msg)


if __name__ == '__main__':
    unittest.main()