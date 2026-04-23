import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.service.dbms_service import DBMS
from src.app import exceptions


class TestCreateDropTable(unittest.TestCase):

    def setUp(self):
        self.dbms = DBMS()
        self.db_name = "test_db_table"
        self.dbms.create_database(self.db_name)
        self.dbms.use_database(self.db_name)

    def tearDown(self):
        DataBase._instances = {}

    def test_create_table_success(self):
        self.dbms.create_table("users", ["id INT", "name TEXT"])
        self.assertTrue(self.dbms.current_db.exist_table("users")) # type: ignore

    def test_create_table_with_columns(self):
        self.dbms.create_table("products", ["id INT", "name TEXT", "price FLOAT"])
        table = self.dbms.current_db.tables["products"] # type: ignore
        self.assertEqual(len(table.metadata.columns), 3)

    def test_create_duplicate_table(self):
        self.dbms.create_table("users", ["id INT"])
        with self.assertRaises(exceptions.TableAlreadyExistsError):
            self.dbms.create_table("users", ["id INT"])

    def test_drop_table_success(self):
        self.dbms.create_table("users", ["id INT"])
        self.dbms.drop_table("users")
        self.assertFalse(self.dbms.current_db.exist_table("users")) # type: ignore

    def test_drop_nonexistent_table(self):
        with self.assertRaises(exceptions.TableNotFoundError):
            self.dbms.drop_table("nonexistent")


if __name__ == '__main__':
    unittest.main()