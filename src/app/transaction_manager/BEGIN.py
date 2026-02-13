from app.controller.database import DataBase

def execute(db: DataBase):
    return db.begin_transaction()
