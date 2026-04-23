import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.main import DBMS
from src.app.controller.database import DataBase


class TestDBMS(unittest.TestCase):

    def setUp(self):
        self.dbms = DBMS()
        DataBase._instances = {}

    def tearDown(self):
        DataBase._instances = {}

    def test_create_database(self):
        success, msg = self.dbms.execute("CREATE_DATABASE test_db")
        self.assertTrue(success)
        self.assertTrue(DataBase.exists("test_db"))

    def test_use_database(self):
        self.dbms.execute("CREATE_DATABASE test_db")
        success, msg = self.dbms.execute("USE test_db")
        self.assertTrue(success)
        self.assertIsNotNone(self.dbms.current_db)

    def test_create_table(self):
        self.dbms.execute("CREATE_DATABASE test_db")
        self.dbms.execute("USE test_db")
        success, msg = self.dbms.execute("CREATE TABLE users (id INT, name TEXT)")
        self.assertTrue(success)

    def test_insert(self):
        self.dbms.execute("CREATE_DATABASE test_db")
        self.dbms.execute("USE test_db")
        self.dbms.execute("CREATE TABLE users (id INT, name TEXT)")
        success, msg = self.dbms.execute("INSERT INTO users VALUES (1, 'Juan')")
        self.assertTrue(success)

    def test_select(self):
        self.dbms.execute("CREATE_DATABASE test_db")
        self.dbms.execute("USE test_db")
        self.dbms.execute("CREATE TABLE users (id INT, name TEXT)")
        self.dbms.execute("INSERT INTO users VALUES (1, 'Juan')")
        success, result = self.dbms.execute("SELECT * FROM users")
        self.assertTrue(success)
        self.assertEqual(len(result), 1)

    def test_select_with_where(self):
        self.dbms.execute("CREATE_DATABASE test_db")
        self.dbms.execute("USE test_db")
        self.dbms.execute("CREATE TABLE users (id INT, name TEXT)")
        self.dbms.execute("INSERT INTO users VALUES (1, 'Juan')")
        self.dbms.execute("INSERT INTO users VALUES (2, 'Maria')")
        success, result = self.dbms.execute("SELECT * FROM users WHERE id = 1")
        self.assertTrue(success)
        self.assertEqual(len(result), 1)

    def test_update(self):
        self.dbms.execute("CREATE_DATABASE test_db")
        self.dbms.execute("USE test_db")
        self.dbms.execute("CREATE TABLE users (id INT, name TEXT)")
        self.dbms.execute("INSERT INTO users VALUES (1, 'Juan')")
        success, msg = self.dbms.execute("UPDATE users SET name = 'Pedro' WHERE id = 1")
        self.assertTrue(success)

    def test_delete(self):
        self.dbms.execute("CREATE_DATABASE test_db")
        self.dbms.execute("USE test_db")
        self.dbms.execute("CREATE TABLE users (id INT, name TEXT)")
        self.dbms.execute("INSERT INTO users VALUES (1, 'Juan')")
        success, msg = self.dbms.execute("DELETE FROM users WHERE id = 1")
        self.assertTrue(success)

    def test_drop_table(self):
        self.dbms.execute("CREATE_DATABASE test_db")
        self.dbms.execute("USE test_db")
        self.dbms.execute("CREATE TABLE users (id INT)")
        success, msg = self.dbms.execute("DROP TABLE users")
        self.assertTrue(success)

    def test_show_databases(self):
        self.dbms.execute("CREATE_DATABASE db1")
        self.dbms.execute("CREATE_DATABASE db2")
        success, result = self.dbms.execute("SHOW_DATABASES")
        self.assertTrue(success)

    def test_show_tables(self):
        self.dbms.execute("CREATE_DATABASE test_db")
        self.dbms.execute("USE test_db")
        self.dbms.execute("CREATE TABLE users (id INT)")
        success, result = self.dbms.execute("SHOW_TABLES")
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()