from src.app.controller.database import DataBase
from src.app.query_processor.USE import get_current_db

def alter_table(db_name: str, table_name: str, action: str, column: str | None = None) -> tuple[bool, str]:
    if db_name:
        db = DataBase.get_instance(db_name)
    else:
        db = get_current_db()
        if db is None:
            return False, "No database selected"
    
    if not db.exist_table(table_name):
        return False, f"Table '{table_name}' does not exist"
    
    if action == "ADD":
        if column:
            db.add_column(table_name, column)
            return True, f"Column '{column}' added to table '{table_name}'"
        return False, "Column name required for ADD action"
    elif action == "DROP":
        table = db.tables[table_name]
        col_names = [col.name for col in table.metadata.columns]
        if column in col_names:
            col_index = col_names.index(column)
            table.metadata.columns.pop(col_index)
            for row in table.records:
                if col_index < len(row):
                    row.pop(col_index)
            return True, f"Column '{column}' dropped from table '{table_name}'"
        return False, f"Column '{column}' does not exist"
    return False, "Invalid action. Use ADD or DROP"