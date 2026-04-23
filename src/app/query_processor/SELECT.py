from src.app.controller.database import DataBase
from src.app.query_processor.USE import get_current_db
from src.app.query_processor.WHERE import apply_where

def select(db_name: str, table_name: str, columns: list | None = None, where_clause: dict | None = None) -> tuple[bool, str | list]:
    if db_name:
        db = DataBase.get_instance(db_name)
    else:
        db = get_current_db()
        if db is None:
            return False, "No database selected"
    
    if not db.exist_table(table_name):
        return False, f"Table '{table_name}' does not exist"
    
    table = db.tables[table_name]
    
    if where_clause:
        records = apply_where(table.records, table.metadata.columns, where_clause)
    else:
        records = table.records
    
    if columns:
        col_indices = []
        col_names = [col.name for col in table.metadata.columns]
        for col in columns:
            if col in col_names:
                col_indices.append(col_names.index(col))
        result = [[row[i] for i in col_indices] for row in records]
    else:
        result = records
    
    return True, result