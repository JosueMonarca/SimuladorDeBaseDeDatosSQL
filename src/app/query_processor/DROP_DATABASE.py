from src.app.controller.database import DataBase

def drop_database(name: str) -> tuple[bool, str]:
    if not DataBase.exists(name):
        return False, f"Database '{name}' does not exist"
    DataBase.remove_instance(name)
    return True, f"Database '{name}' dropped successfully"