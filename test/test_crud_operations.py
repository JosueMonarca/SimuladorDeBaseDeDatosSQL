import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.query_processor.CREATE_TABLE import create_table
from src.app.query_processor.INSERT import insert
from src.app.query_processor.SELECT import select
from src.app.query_processor.UPDATE import update
from src.app.query_processor.DELETE import delete


class TestInsert(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_insert"
        DataBase.get_instance(self.db_name)
        create_table(self.db_name, "users", ["id INT", "name TEXT"])

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_insert_single_record(self):
        success, msg = insert(self.db_name, "users", ["1", "Juan"])
        self.assertTrue(success)
        db = DataBase.get_instance(self.db_name)
        self.assertEqual(len(db.tables["users"].records), 1)

    def test_insert_multiple_records(self):
        insert(self.db_name, "users", ["1", "Juan"])
        insert(self.db_name, "users", ["2", "Maria"])
        db = DataBase.get_instance(self.db_name)
        self.assertEqual(len(db.tables["users"].records), 2)

    def test_insert_into_nonexistent_table(self):
        success, msg = insert(self.db_name, "nonexistent", ["1", "Juan"])
        self.assertFalse(success)


class TestSelect(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_select"
        DataBase.get_instance(self.db_name)
        create_table(self.db_name, "users", ["id INT", "name TEXT"])
        insert(self.db_name, "users", ["1", "Juan"])
        insert(self.db_name, "users", ["2", "Maria"])

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_select_all(self):
        success, result = select(self.db_name, "users")
        self.assertTrue(success)
        self.assertEqual(len(result), 2)

    def test_select_with_where(self):
        success, result = select(self.db_name, "users", where_clause={"column": "id", "operator": "=", "value": 1})
        self.assertTrue(success)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)

    def test_select_nonexistent_table(self):
        success, msg = select(self.db_name, "nonexistent")
        self.assertFalse(success)


class TestUpdate(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_update"
        DataBase.get_instance(self.db_name)
        create_table(self.db_name, "users", ["id INT", "name TEXT"])
        insert(self.db_name, "users", ["1", "Juan"])
        insert(self.db_name, "users", ["2", "Maria"])

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_update_with_where(self):
        success, msg = update(self.db_name, "users", {"column": "name", "value": "Pedro"}, {"column": "id", "operator": "=", "value": 1})
        self.assertTrue(success)
        db = DataBase.get_instance(self.db_name)
        self.assertEqual(db.tables["users"].records[0][1], "Pedro")

    def test_update_without_where(self):
        success, msg = update(self.db_name, "users", {"column": "name", "value": "Unknown"}, None)
        self.assertTrue(success)


class TestDelete(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_delete"
        DataBase.get_instance(self.db_name)
        create_table(self.db_name, "users", ["id INT", "name TEXT"])
        insert(self.db_name, "users", ["1", "Juan"])
        insert(self.db_name, "users", ["2", "Maria"])

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_delete_with_where(self):
        success, msg = delete(self.db_name, "users", {"column": "id", "operator": "=", "value": 1})
        self.assertTrue(success)
        db = DataBase.get_instance(self.db_name)
        self.assertEqual(len(db.tables["users"].records), 1)

    def test_delete_all(self):
        success, msg = delete(self.db_name, "users", None)
        self.assertTrue(success)
        db = DataBase.get_instance(self.db_name)
        self.assertEqual(len(db.tables["users"].records), 0)


if __name__ == '__main__':
    unittest.main()