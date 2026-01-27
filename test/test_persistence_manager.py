import unittest
import sys
import os

# Asegurar que Python encuentre la carpeta App
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.persistence.PersistenceManager import PersistenceManager
from app.database import DataBase

class TestPersistenceManager(unittest.TestCase):
    def setUp(self):
        self.persistence_manager = PersistenceManager()

    def test_save_and_load(self):
        # Crear una base de datos de prueba
        db = DataBase()
        db.add_table("prueba")
        db.add_column("prueba", "columna")
        db.add_record("prueba", ["valor"])

        # Guardar la base de datos
        self.persistence_manager.save_db(db)

        # Cargar la base de datos
        loaded_db = self.persistence_manager.load_db()

        # Verificar que la base de datos cargada sea la misma que la guardada
        self.assertEqual(db.tables["prueba"].metadata, loaded_db.tables["prueba"].metadata)
        self.assertEqual(db.tables["prueba"].records, loaded_db.tables["prueba"].records)

    def tearDown(self):
        # Limpiar archivos de prueba
        self.persistence_manager.delete_db()