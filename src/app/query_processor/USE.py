from src.app.controller.database import DataBase


def use(db_name: str) -> DataBase:
    if not DataBase.exists(db_name):
        from src.app.exceptions import DatabaseNotFoundError
        raise DatabaseNotFoundError(f"Database '{db_name}' does not exist")
    return DataBase.get_instance(db_name)


def get_current_db() -> DataBase | None:
    return None