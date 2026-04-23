import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.transaction_manager.TransactionManager import TransactionManager


class TestTransactionManager(unittest.TestCase):

    def setUp(self):
        self.db = DataBase()
        self.tm = TransactionManager(self.db)

    def test_begin_transaction(self):
        self.db.add_table("test")
        self.db.add_column("test", "col1")
        self.db.add_record("test", ["value1"])
        
        result = self.tm.begin()
        
        self.assertTrue(result)
        self.assertTrue(self.tm.is_in_transaction())

    def test_begin_already_in_transaction(self):
        self.tm.begin()
        result = self.tm.begin()
        
        self.assertFalse(result)
        self.assertTrue(self.tm.is_in_transaction())

    def test_commit_transaction(self):
        self.tm.begin()
        result = self.tm.commit()
        
        self.assertTrue(result)
        self.assertFalse(self.tm.is_in_transaction())

    def test_commit_without_transaction(self):
        result = self.tm.commit()
        
        self.assertFalse(result)
        self.assertFalse(self.tm.is_in_transaction())

    def test_rollback_transaction(self):
        self.db.add_table("test")
        self.db.add_column("test", "col1")
        self.db.add_record("test", ["value1"])
        
        self.tm.begin()
        self.db.add_record("test", ["value2"])
        
        result = self.tm.rollback()
        
        self.assertTrue(result)
        self.assertFalse(self.tm.is_in_transaction())
        self.assertEqual(len(self.db.tables["test"].records), 1)
        self.assertEqual(self.db.tables["test"].records[0], ["value1"])

    def test_rollback_without_transaction(self):
        result = self.tm.rollback()
        
        self.assertFalse(result)
        self.assertFalse(self.tm.is_in_transaction())

    def test_rollback_removes_added_data(self):
        self.db.add_table("test")
        self.db.add_column("test", "col1")
        
        self.tm.begin()
        self.db.add_table("new_table")
        
        self.tm.rollback()
        
        self.assertFalse(self.db.exist_table("new_table"))
        self.assertTrue(self.db.exist_table("test"))

    def test_commit_persists_changes(self):
        self.db.add_table("test")
        self.db.add_column("test", "col1")
        
        self.tm.begin()
        self.db.add_record("test", ["value1"])
        self.tm.commit()
        
        self.assertEqual(len(self.db.tables["test"].records), 1)
        
        result = self.tm.rollback()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()