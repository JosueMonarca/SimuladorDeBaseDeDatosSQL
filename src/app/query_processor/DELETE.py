from src.app.controller.database import DataBase
from src.app.query_processor.WHERE import apply_where


def delete(db_name: str, table_name: str, where_clause: dict | None = None) -> int:
    db = DataBase.get_instance(db_name)
    
    if not db.exist_table(table_name):
        from src.app.exceptions import TableNotFoundError
        raise TableNotFoundError(f"Table '{table_name}' does not exist")
    
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
    
    return deleted_count