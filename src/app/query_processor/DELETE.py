from src.app.controller.database import DataBase
from src.app.query_processor.USE import get_current_db
from src.app.query_processor.WHERE import apply_where

def delete(db_name: str, table_name: str, where_clause: dict | None = None) -> tuple[bool, str]:
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
        records_to_delete = apply_where(table.records, table.metadata.columns, where_clause)
    else:
        records_to_delete = table.records
    
    deleted_count = len(records_to_delete)
    
    if where_clause:
        table.records = [r for r in table.records if r not in records_to_delete]
    else:
        table.records = []
    
    return True, f"{deleted_count} record(s) deleted"