import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.controller.database import DataBase
from src.app.query_processor.CREATE_TABLE import create_table
from src.app.query_processor.INSERT import insert
from src.app.query_processor.WHERE import apply_where
from src.app.data_dictionary.__dictionary__ import metadata_column


class TestWhere(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db_where"
        DataBase.get_instance(self.db_name)
        create_table(self.db_name, "users", ["id INT", "name TEXT", "age INT"])
        insert(self.db_name, "users", ["1", "Juan", "25"])
        insert(self.db_name, "users", ["2", "Maria", "30"])
        insert(self.db_name, "users", ["3", "Pedro", "25"])
        self.db = DataBase.get_instance(self.db_name)
        self.table = self.db.tables["users"]
        self.columns = self.table.metadata.columns

    def tearDown(self):
        DataBase.remove_instance(self.db_name)

    def test_where_equals(self):
        result = apply_where(self.table.records, self.columns, {"column": "id", "operator": "=", "value": 1})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)

    def test_where_not_equals(self):
        result = apply_where(self.table.records, self.columns, {"column": "id", "operator": "!=", "value": 1})
        self.assertEqual(len(result), 2)

    def test_where_greater_than(self):
        result = apply_where(self.table.records, self.columns, {"column": "age", "operator": ">", "value": 25})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][2], 30)

    def test_where_less_than(self):
        result = apply_where(self.table.records, self.columns, {"column": "age", "operator": "<", "value": 30})
        self.assertEqual(len(result), 2)

    def test_where_greater_equal(self):
        result = apply_where(self.table.records, self.columns, {"column": "age", "operator": ">=", "value": 25})
        self.assertEqual(len(result), 3)

    def test_where_less_equal(self):
        result = apply_where(self.table.records, self.columns, {"column": "age", "operator": "<=", "value": 25})
        self.assertEqual(len(result), 2)

    def test_where_nonexistent_column(self):
        result = apply_where(self.table.records, self.columns, {"column": "nonexistent", "operator": "=", "value": 1})
        self.assertEqual(len(result), 3)


if __name__ == '__main__':
    unittest.main()