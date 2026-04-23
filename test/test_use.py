import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.service.dbms_service import DBMS


class TestUse(unittest.TestCase):

    def setUp(self):
        self.dbms = DBMS()
        self.db_name = "test_db_use"
        self.dbms.create_database(self.db_name)

    def tearDown(self):
        DataBase._instances = {}

    def test_use_existing_database(self):
        db = self.dbms.use_database(self.db_name)
        self.assertIsNotNone(self.dbms.current_db)

    def test_use_nonexistent_database(self):
        with self.assertRaises(Exception):
            self.dbms.use_database("nonexistent_db")


if __name__ == '__main__':
    unittest.main()