from src.app.controller.database import DataBase

def create_database(name: str) -> tuple[bool, str]:
    if DataBase.exists(name):
        return False, f"Database '{name}' already exists"
    DataBase.get_instance(name)
    return True, f"Database '{name}' created successfully"