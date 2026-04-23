from typing import Optional
from src.app.controller.database import DataBase
from src.app.query_processor.USE import get_current_db
from src.app.query_processor.WHERE import apply_where

def update(db_name: str, table_name: str, set_clause: dict, where_clause: Optional[dict] = None) -> tuple[bool, str]:
    if db_name:
        db = DataBase.get_instance(db_name)
    else:
        db = get_current_db()
        if db is None:
            return False, "No database selected"
    
    if not db.exist_table(table_name):
        return False, f"Table '{table_name}' does not exist"
    
    table = db.tables[table_name]
    col_names = [col.name for col in table.metadata.columns]
    
    set_col = set_clause.get("column")
    set_value = set_clause.get("value")
    
    if set_col not in col_names:
        return False, f"Column '{set_col}' does not exist"
    
    col_index = col_names.index(set_col)
    
    if where_clause:
        records = apply_where(table.records, table.metadata.columns, where_clause)
    else:
        records = table.records
    
    updated_count = 0
    for record in records:
        record[col_index] = set_value
        updated_count += 1
    
    return True, f"{updated_count} record(s) updated"