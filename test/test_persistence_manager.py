import unittest
import sys
import os
import json

# Asegurar que Python encuentre la carpeta App
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.storage_manager.persistence_manager import PersistenceManager
from app.controller.database import DataBase

class TestPersistenceManager(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        if os.path.exists("test_db.json"):
            os.remove("test_db.json")
    
    def setUp(self):
        #self.persistence_manager = PersistenceManager()
        # Prueva cargar y guardar una base de datos simple;
        self.db = DataBase()
        self.db.add_table("test_table")
        self.db.add_column("test_table", "column1")
        self.db.add_record("test_table", ["value1"])
        self.filepath = "test_db.json"
        
    def tearDown(self) -> None:
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        
    def test_save_file(self):
        PersistenceManager.save_db(self.db, self.filepath)
        # Verificar que el archivo se haya creado 
        self.assertTrue(os.path.exists(self.filepath))
        
    def test_save_file_content(self):
        PersistenceManager.save_db(self.db, self.filepath)
            
        with open(self.filepath, "r") as f:
            actual_data = json.load(f)
            expected_data= {
                "test_table": {
                    "columns": ["column1"],
                    "records": [["value1"]]
                }
            }
            self.assertEqual(actual_data, expected_data)
            
    def test_load_file (self):
        PersistenceManager.save_db(self.db, self.filepath)
        
        loader_file = PersistenceManager.load_db(self.filepath)
        #print(loader_file.tables)
        self.assertTrue(loader_file.exist_table("test_table"))
        #self.assertEqual(loader_file.tables["test_table"].columns["column1"], ["column1"])
        self.assertEqual(loader_file.tables["test_table"].records, [["value1"]])
        
    def test_load_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            PersistenceManager.load_db("non_existent_file.json")
    
    def test_load_corrupted_file(self):
        # Caso 1: texto plano (el más claro para leer el test)
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("contenido corrupto - no es json")
    
        with self.assertRaises(json.JSONDecodeError):
            PersistenceManager.load_db(self.filepath)
    
        # Opcional: segundo caso dentro del mismo test (coma extra)
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write('{"test_table": {"columns": ["col1"], "records": [["a"]] }, }')
    
        with self.assertRaises(json.JSONDecodeError):
            PersistenceManager.load_db(self.filepath)
    
    def test_save_empty_db(self):
        with open(self.filepath,"w") as f:
            json.dump(DataBase().to_dict(), f, indent = 4)
            
if __name__ == '__main__':
    unittest.main()