import json
import os
from app.controller.database import DataBase

class PersistenceManager:
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def save_db( db: DataBase, filepath: str) -> None:
        with open (filepath, "w") as f:
            json.dump(db.to_dict(), f, indent = 4)

    @staticmethod
    def load_db( filepath: str) -> DataBase:
        with open (filepath, "r") as f:
            data_dict = json.load(f)
            return DataBase.from_dict(data_dict)

    @staticmethod
    def delete_db(filepath: str) -> None:
        if os.path.exists (filepath):
            os.remove(filepath)