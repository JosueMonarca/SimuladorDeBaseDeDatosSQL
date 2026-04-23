from src.app.controller.database import DataBase


def drop_database(name: str) -> None:
    if not DataBase.exists(name):
        from src.app.exceptions import DatabaseNotFoundError
        raise DatabaseNotFoundError(f"Database '{name}' does not exist")
    DataBase.remove_instance(name)