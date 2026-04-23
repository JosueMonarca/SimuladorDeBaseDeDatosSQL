from src.app.controller.database import DataBase


def select(db_name: str, table_name: str, columns: list | None = None, where_clause: dict | None = None) -> list:
    db = DataBase.get_instance(db_name)
    
    if not db.exist_table(table_name):
        from src.app.exceptions import TableNotFoundError
        raise TableNotFoundError(f"Table '{table_name}' does not exist")
    
    table = db.tables[table_name]
    
    from src.app.query_processor.WHERE import apply_where
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
        return [[row[i] for i in col_indices] for row in records]
    else:
        return records