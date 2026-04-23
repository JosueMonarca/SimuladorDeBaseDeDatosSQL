import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.query_processor.CREATE_DATABASE import create_database
from src.app.query_processor.DROP_DATABASE import drop_database


class TestCreateDatabase(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_create"
        DataBase.remove_instance(self.db_name)

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_create_database_success(self):
        success, msg = create_database(self.db_name)
        self.assertTrue(success)
        self.assertIn("created successfully", msg)
        self.assertTrue(DataBase.exists(self.db_name))

    def test_create_duplicate_database(self):
        create_database(self.db_name)
        success, msg = create_database(self.db_name)
        self.assertFalse(success)
        self.assertIn("already exists", msg)


class TestDropDatabase(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_drop"
        DataBase.get_instance(self.db_name)

    def test_drop_database_success(self):
        success, msg = drop_database(self.db_name)
        self.assertTrue(success)
        self.assertIn("dropped successfully", msg)
        self.assertFalse(DataBase.exists(self.db_name))

    def test_drop_nonexistent_database(self):
        success, msg = drop_database("nonexistent_db")
        self.assertFalse(success)
        self.assertIn("does not exist", msg)


if __name__ == '__main__':
    unittest.main()