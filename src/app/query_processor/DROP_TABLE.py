from src.app.controller.database import DataBase

def drop_table(db_name: str, table_name: str) -> tuple[bool, str]:
    db = DataBase.get_instance(db_name)
    if not db.exist_table(table_name):
        return False, f"Table '{table_name}' does not exist in database '{db_name}'"
    del db.tables[table_name]
    return True, f"Table '{table_name}' dropped successfully"