from src.app.controller.database import DataBase
from src.app.query_processor.CREATE_DATABASE import create_database

def create_table(db_name: str, table_name: str, columns: list[str]) -> tuple[bool, str]:
    db = DataBase.get_instance(db_name)
    if db.add_table(table_name):
        for col in columns:
            col_parts = col.strip().split()
            col_name = col_parts[0]
            col_type = str
            if len(col_parts) > 1:
                type_str = col_parts[1].upper()
                if type_str == "INT":
                    col_type = int
                elif type_str == "FLOAT":
                    col_type = float
            db.add_column(table_name, col_name, col_type=col_type)
        return True, f"Table '{table_name}' created successfully"
    return False, f"Table '{table_name}' already exists in database '{db_name}'"