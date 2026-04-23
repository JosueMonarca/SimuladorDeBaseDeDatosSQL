import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.query_processor.CREATE_TABLE import create_table
from src.app.query_processor.ALTER_TABLE import alter_table


class TestAlterTable(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_alter"
        DataBase.get_instance(self.db_name)
        create_table(self.db_name, "users", ["id INT", "name TEXT"])

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_alter_add_column(self):
        success, msg = alter_table(self.db_name, "users", "ADD", "email")
        self.assertTrue(success)
        db = DataBase.get_instance(self.db_name)
        self.assertEqual(len(db.tables["users"].metadata.columns), 3)

    def test_alter_drop_column(self):
        alter_table(self.db_name, "users", "ADD", "email")
        success, msg = alter_table(self.db_name, "users", "DROP", "email")
        self.assertTrue(success)
        db = DataBase.get_instance(self.db_name)
        self.assertEqual(len(db.tables["users"].metadata.columns), 2)

    def test_alter_nonexistent_table(self):
        success, msg = alter_table(self.db_name, "nonexistent", "ADD", "col")
        self.assertFalse(success)

    def test_alter_drop_nonexistent_column(self):
        success, msg = alter_table(self.db_name, "users", "DROP", "nonexistent")
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()