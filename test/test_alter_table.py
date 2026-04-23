import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.service.dbms_service import DBMS
from src.app import exceptions


class TestAlterTable(unittest.TestCase):

    def setUp(self):
        self.dbms = DBMS()
        self.db_name = "test_db_alter"
        self.dbms.create_database(self.db_name)
        self.dbms.use_database(self.db_name)
        self.dbms.create_table("users", ["id INT", "name TEXT"])

    def tearDown(self):
        DataBase._instances = {}

    def test_alter_add_column(self):
        self.dbms.alter_table("users", "ADD", "email")
        self.assertEqual(len(self.dbms.current_db.tables["users"].metadata.columns), 3) # type: ignore

    def test_alter_drop_column(self):
        self.dbms.alter_table("users", "ADD", "email")
        self.dbms.alter_table("users", "DROP", "email")
        self.assertEqual(len(self.dbms.current_db.tables["users"].metadata.columns), 2) # type: ignore

    def test_alter_nonexistent_table(self):
        with self.assertRaises(exceptions.TableNotFoundError):
            self.dbms.alter_table("nonexistent", "ADD", "col")

    def test_alter_drop_nonexistent_column(self):
        with self.assertRaises(exceptions.ColumnNotFoundError):
            self.dbms.alter_table("users", "DROP", "nonexistent")


if __name__ == '__main__':
    unittest.main()