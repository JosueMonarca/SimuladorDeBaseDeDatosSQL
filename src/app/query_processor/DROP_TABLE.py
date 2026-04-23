from src.app.controller.database import DataBase


def drop_table(db_name: str, table_name: str) -> None:
    db = DataBase.get_instance(db_name)
    if not db.exist_table(table_name):
        from src.app.exceptions import TableNotFoundError
        raise TableNotFoundError(f"Table '{table_name}' does not exist in database '{db_name}'")
    del db.tables[table_name]