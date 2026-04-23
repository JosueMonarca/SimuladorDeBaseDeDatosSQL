from src.app.controller.database import DataBase


def alter_table(db_name: str, table_name: str, action: str, column: str | None = None) -> None:
    db = DataBase.get_instance(db_name)
    
    if not db.exist_table(table_name):
        from src.app.exceptions import TableNotFoundError
        raise TableNotFoundError(f"Table '{table_name}' does not exist")
    
    if action == "ADD":
        if not column:
            from src.app.exceptions import ColumnError
            raise ColumnError("Column name required for ADD action")
        db.add_column(table_name, column)
    elif action == "DROP":
        table = db.tables[table_name]
        col_names = [col.name for col in table.metadata.columns]
        if column not in col_names:
            from src.app.exceptions import ColumnNotFoundError
            raise ColumnNotFoundError(f"Column '{column}' does not exist")
        col_index = col_names.index(column)
        table.metadata.columns.pop(col_index)
        for row in table.records:
            if col_index < len(row):
                row.pop(col_index)
    else:
        from src.app.exceptions import ColumnError
        raise ColumnError("Invalid action. Use ADD or DROP")