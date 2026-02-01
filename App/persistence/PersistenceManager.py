import json
import os
from app.database import DataBase

class PersistenceManager:
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def save_db( db: DataBase, filepath: str) -> None:
        with open (filepath, "w") as f:
            json.dump(db.to_dict(), f, indent = 4)

    @staticmethod
    def load_db( filepath: str) -> DataBase:
        return DataBase.from_dict(json.load(open (filepath, "r")))

    @staticmethod
    def delete_db(filepath: str) -> None:
        if os.path.exists (filepath):
            os.remove(filepath)