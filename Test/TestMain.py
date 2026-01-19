import unittest
import sys
import os

# Asegurar que Python encuentre la carpeta App
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from App.main import DataBase
from App.table import Table

class TestDBMS(unittest.TestCase):

    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.db = DataBase()

    # --- Pruebas de la clase Table ---
    
    def test_add_column_unique_name(self):
        """Verifica que no se repitan nombres de columnas en una tabla"""
        tabla = Table("test")
        tabla.add_column("ID")
        tabla.add_column("ID") # Intento repetido
        self.assertEqual(len(tabla.metadata), 1)

    def test_record_validation_type(self):
        """Verifica que se respete el tipo de dato (isinstance)"""
        tabla = Table("empleados")
        tabla.add_column("Edad", type=int)
        # Intentar insertar un string donde va un entero
        resultado = tabla.add_record(["Veinte"]) 
        self.assertFalse(resultado)

    def test_record_uniqueness(self):
        """Verifica la restricción de unicidad (unique=True)"""
        tabla = Table("clientes")
        tabla.add_column("Email", unique=True)
        tabla.add_record(["test@mail.com"])
        # Intentar insertar el mismo correo
        resultado = tabla.add_record(["test@mail.com"])
        self.assertFalse(resultado)

    # --- Pruebas de la clase DataBase ---

    def test_create_duplicate_table(self):
        """Verifica que DataBase no permita tablas con el mismo nombre"""
        self.db.add_table("ventas")
        resultado = self.db.add_table("ventas")
        self.assertFalse(resultado)

    def test_add_record_to_db(self):
        """Prueba el flujo completo: Crear tabla, columna e insertar registro"""
        self.db.add_table("stock")
        self.db.add_column("stock", "Cantidad")
        resultado = self.db.add_record("stock", [50])
        self.assertTrue(resultado)

    def test_exist_table(self):
        """Verifica el funcionamiento del buscador de tablas"""
        self.db.add_table("inventario")
        self.assertTrue(self.db.exist_table("inventario"))
        self.assertFalse(self.db.exist_table("no_existe"))

if __name__ == '__main__':
    unittest.main()