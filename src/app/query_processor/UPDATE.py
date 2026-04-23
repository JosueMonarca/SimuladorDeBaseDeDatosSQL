from src.app.controller.database import DataBase
from src.app.query_processor.WHERE import apply_where


def update(db_name: str, table_name: str, set_clause: dict, where_clause: dict | None = None) -> int:
    db = DataBase.get_instance(db_name)
    
    if not db.exist_table(table_name):
        from src.app.exceptions import TableNotFoundError
        raise TableNotFoundError(f"Table '{table_name}' does not exist")
    
    table = db.tables[table_name]
    col_names = [col.name for col in table.metadata.columns]
    
    set_col = set_clause.get("column")
    set_value = set_clause.get("value")
    
    if set_col not in col_names:
        from src.app.exceptions import ColumnNotFoundError
        raise ColumnNotFoundError(f"Column '{set_col}' does not exist")
    
    col_index = col_names.index(set_col)
    
    if where_clause:
        records = apply_where(table.records, table.metadata.columns, where_clause)
    else:
        records = table.records
    
    updated_count = 0
    for record in records:
        record[col_index] = set_value
        updated_count += 1
    
    return updated_count