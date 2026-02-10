import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controller.database import DataBase
from app.controller.table import Table

class TestDBMS(unittest.TestCase):

    def setUp(self):
        self.db = DataBase()
    
    def test_add_column_unique_name(self):
        tabla = Table("test")
        tabla.add_column("ID")
        tabla.add_column("ID")
        self.assertEqual(len(tabla.metadata.columns), 1)

    def test_record_validation_type(self):
        tabla = Table("empleados")
        tabla.add_column("Edad", col_type=int)
        resultado = tabla.add_record(["Veinte"]) 
        self.assertFalse(resultado)

    def test_record_uniqueness(self):
        tabla = Table("clientes")
        tabla.add_column("Email", unique=True)
        tabla.add_record(["test@mail.com"])
        resultado = tabla.add_record(["test@mail.com"])
        self.assertFalse(resultado)

    def test_create_duplicate_table(self):
        self.db.add_table("ventas")
        resultado = self.db.add_table("ventas")
        self.assertFalse(resultado)

    def test_add_record_to_db(self):
        self.db.add_table("stock")
        self.db.add_column("stock", "Cantidad")
        resultado = self.db.add_record("stock", [50])
        self.assertTrue(resultado)

    def test_exist_table(self):
        self.db.add_table("inventario")
        self.assertTrue(self.db.exist_table("inventario"))
        self.assertFalse(self.db.exist_table("no_existe"))

if __name__ == '__main__':
    unittest.main()