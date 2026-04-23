import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.query_processor.USE import use, get_current_db, set_current_db
from src.app.query_processor.CREATE_DATABASE import create_database


class TestUse(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_use"
        create_database(self.db_name)

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_use_existing_database(self):
        success, msg = use(self.db_name)
        self.assertTrue(success)
        self.assertIn("Using database", msg)
        self.assertIsNotNone(get_current_db())

    def test_use_nonexistent_database(self):
        success, msg = use("nonexistent_db")
        self.assertFalse(success)
        self.assertIn("does not exist", msg)

    def test_set_current_db(self):
        db = DataBase.get_instance(self.db_name)
        set_current_db(db)
        self.assertEqual(get_current_db(), db)


if __name__ == '__main__':
    unittest.main()