import sys
import os
import unittest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from app.controller.database import DataBase
from app.query_processor.manager import QueryProcessor

class TestDatabaseSimulation(unittest.TestCase):
    def setUp(self):
        self.db = DataBase()
        self.processor = QueryProcessor(self.db)

    def test_create_and_insert(self):
        self.processor.execute("CREATE TABLE users (id int, name str)")
        result = self.processor.execute("INSERT INTO users VALUES (1, 'Alice')")
        self.assertEqual(result, "Record inserted successfully.")
        
        select_result = self.processor.execute("SELECT * FROM users")
        self.assertIn("[1, 'Alice']", select_result)

    def test_transaction_commit(self):
        self.processor.execute("CREATE TABLE products (id int, name str)")
        self.processor.execute("BEGIN TRANSACTION")
        self.processor.execute("INSERT INTO products VALUES (1, 'Laptop')")
        self.processor.execute("COMMIT TRANSACTION")
        
        select_result = self.processor.execute("SELECT * FROM products")
        self.assertIn("[1, 'Laptop']", select_result)

    def test_transaction_rollback(self):
        self.processor.execute("CREATE TABLE orders (id int)")
        self.processor.execute("BEGIN TRANSACTION")
        self.processor.execute("INSERT INTO orders VALUES (100)")
        select_pending = self.processor.execute("SELECT * FROM orders")
        self.assertIn("[100]", select_pending)
        
        self.processor.execute("ROLLBACK TRANSACTION")
        select_final = self.processor.execute("SELECT * FROM orders")
        self.assertNotIn("[100]", select_final)

    def test_save_load(self):
        self.processor.execute("CREATE TABLE setup (id int)")
        self.processor.execute("INSERT INTO setup VALUES (1)")
        self.processor.execute("SAVE DATABASE test_db.json")
        
        # clearer simulation state
        self.db = DataBase()
        self.processor = QueryProcessor(self.db)
        
        load_result = self.processor.execute("LOAD DATABASE test_db.json")
        self.assertIn("Database loaded", load_result)
        
        select_result = self.processor.execute("SELECT * FROM setup")
        self.assertIn("[1]", select_result)
        
        # Cleanup
        if os.path.exists("test_db.json"):
            os.remove("test_db.json")

    def test_delete_update_drop(self):
        self.processor.execute("CREATE TABLE items (id int, name str, price int)")
        self.processor.execute("INSERT INTO items VALUES (1, 'A', 10)")
        self.processor.execute("INSERT INTO items VALUES (2, 'B', 20)")
        self.processor.execute("INSERT INTO items VALUES (3, 'C', 30)")
        
        # Test UPDATE
        update_res = self.processor.execute("UPDATE items SET price=25 WHERE id = 2")
        self.assertIn("1 record(s) updated", update_res)
        select_res = self.processor.execute("SELECT * FROM items")
        self.assertIn("[2, 'B', 25]", select_res)
        
        # Test DELETE
        delete_res = self.processor.execute("DELETE FROM items WHERE price > 20")
        # Should delete items with price 25 (id 2) and 30 (id 3)
        self.assertIn("2 record(s) deleted", delete_res)
        select_res_2 = self.processor.execute("SELECT * FROM items")
        self.assertNotIn("[2, 'B', 25]", select_res_2)
        self.assertNotIn("[3, 'C', 30]", select_res_2)
        self.assertIn("[1, 'A', 10]", select_res_2)
        
        # Test DROP TABLE
        drop_res = self.processor.execute("DROP TABLE items")
        self.assertIn("dropped successfully", drop_res)
        drop_err = self.processor.execute("DROP TABLE items")
        self.assertIn("Error", drop_err)

    def test_system_commands(self):
        # ALTER TABLE
        self.processor.execute("CREATE TABLE users (name str)")
        self.processor.execute("INSERT INTO users VALUES ('Bob')")
        alter_res = self.processor.execute("ALTER TABLE users ADD age int")
        self.assertIn("altered successfully", alter_res)
        
        # Verify column added (records padded with None? existing logic check)
        # Table.add_column pads with None.
        select_res = self.processor.execute("SELECT * FROM users")
        # ['Bob', None]
        self.assertIn("None", select_res)
        
        # DB Management
        create_db_res = self.processor.execute("CREATE DATABASE test_sys_db")
        self.assertIn("created successfully", create_db_res)
        
        # Switch to it
        use_res = self.processor.execute("USE test_sys_db")
        self.assertIn("Switched to", use_res)
        
        # Verify empty state
        self.assertEqual(len(self.db.tables), 0)
        
        # Switch back or clean up
        # We need to drop it. But we are "inside" it? 
        # PersistenceManager operations act on filepaths.
        
        # Drop it
        drop_db_res = self.processor.execute("DROP DATABASE test_sys_db")
        self.assertIn("dropped successfully", drop_db_res)

        # Cleanup
        if os.path.exists("test_sys_db.json"):
            os.remove("test_sys_db.json")

if __name__ == '__main__':
    unittest.main()
