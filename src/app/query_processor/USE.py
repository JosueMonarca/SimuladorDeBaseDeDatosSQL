from src.app.controller.database import DataBase

_current_db = None

def use(db_name: str) -> tuple[bool, str]:
    global _current_db
    if not DataBase.exists(db_name):
        return False, f"Database '{db_name}' does not exist"
    _current_db = DataBase.get_instance(db_name)
    return True, f"Using database '{db_name}'"

def get_current_db() -> 'DataBase | None':
    return _current_db

def set_current_db(db: DataBase):
    global _current_db
    _current_db = db