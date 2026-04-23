from src.app.controller.database import DataBase


def create_table(db_name: str, table_name: str, columns: list[str]) -> None:
    db = DataBase.get_instance(db_name)
    if not db.add_table(table_name):
        from src.app.exceptions import TableAlreadyExistsError
        raise TableAlreadyExistsError(f"Table '{table_name}' already exists in database '{db_name}'")
    
    for col in columns:
        col_parts = col.strip().split()
        col_name = col_parts[0]
        col_type = None
        if len(col_parts) > 1:
            type_str = col_parts[1].upper()
            if type_str == "INT":
                col_type = int
            elif type_str == "FLOAT":
                col_type = float
        db.add_column(table_name, col_name, col_type=col_type)


def drop_table(db_name: str, table_name: str) -> None:
    db = DataBase.get_instance(db_name)
    if not db.exist_table(table_name):
        from src.app.exceptions import TableNotFoundError
        raise TableNotFoundError(f"Table '{table_name}' does not exist in database '{db_name}'")
    del db.tables[table_name]