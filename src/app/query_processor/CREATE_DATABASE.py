from src.app.controller.database import DataBase


def create_database(name: str) -> DataBase:
    if DataBase.exists(name):
        from src.app.exceptions import DatabaseAlreadyExistsError
        raise DatabaseAlreadyExistsError(f"Database '{name}' already exists")
    return DataBase.get_instance(name)


def drop_database(name: str) -> None:
    if not DataBase.exists(name):
        from src.app.exceptions import DatabaseNotFoundError
        raise DatabaseNotFoundError(f"Database '{name}' does not exist")
    DataBase.remove_instance(name)