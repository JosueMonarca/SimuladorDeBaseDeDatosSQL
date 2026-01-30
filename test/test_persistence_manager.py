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

    