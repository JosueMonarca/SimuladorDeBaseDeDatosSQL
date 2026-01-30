import json
from app.database import DataBase

class PersistenceManager:
    
    def __init__(self) -> None:
        pass

    def save_db(self, db: DataBase) -> None:
        json_data = json.dumps(db)
        

    def load_db(self):# -> DataBase:
        pass

    def delete_db(self) -> None:
        pass