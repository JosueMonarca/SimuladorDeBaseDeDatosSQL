import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.main import DBMS
from src.app.controller.database import DataBase
from src.app.transaction_manager.BEGIN import begin
from src.app.transaction_manager.COMMIT import commit
from src.app.transaction_manager.ROLLBACK import rollback


class TestTransactionIntegration(unittest.TestCase):

    def setUp(self):
        self.dbms = DBMS()
        DataBase._instances = {}
        self.dbms.execute("CREATE_DATABASE test_db")
        self.dbms.execute("USE test_db")
        self.dbms.execute("CREATE TABLE users (id INT, name TEXT)")
        self.dbms.execute("INSERT INTO users VALUES (1, 'Juan')")

    def tearDown(self):
        DataBase._instances = {}

    def test_begin_transaction(self):
        success, msg = self.dbms.execute("BEGIN")
        self.assertTrue(success)
        self.assertTrue(self.dbms.transaction_manager.is_in_transaction())

    def test_commit_transaction(self):
        self.dbms.execute("BEGIN")
        self.dbms.execute("INSERT INTO users VALUES (2, 'Maria')")
        success, msg = self.dbms.execute("COMMIT")
        self.assertTrue(success)
        self.assertEqual(len(self.dbms.current_db.tables["users"].records), 2)

    def test_rollback_transaction(self):
        self.dbms.execute("BEGIN")
        self.dbms.execute("INSERT INTO users VALUES (2, 'Maria')")
        success, msg = self.dbms.execute("ROLLBACK")
        self.assertTrue(success)
        self.assertEqual(len(self.dbms.current_db.tables["users"].records), 1)

    def test_rollback_restores_original_data(self):
        self.dbms.execute("BEGIN")
        self.dbms.execute("UPDATE users SET name = 'Pedro' WHERE id = 1")
        self.dbms.execute("ROLLBACK")
        self.assertEqual(self.dbms.current_db.tables["users"].records[0][1], "Juan")

    def test_begin_without_db(self):
        dbms2 = DBMS()
        success, msg = dbms2.execute("BEGIN")
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()