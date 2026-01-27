import json
from app.database import DataBase

class PersistenceManager:
    
    def __init__(self) -> None:
        self.json = json
 
    def save_db(self, db: DataBase) -> None:
        pass

    def load_db(self) -> DataBase:
        pass

    def delete_db(self) -> None:
        pass