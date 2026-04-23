from src.app.controller.database import DataBase

def from_clause(table_name: str, db_name: str | None = None) -> tuple[bool, str | object]:
    if db_name:
        db = DataBase.get_instance(db_name)
    else:
        from src.app.query_processor.USE import get_current_db
        db = get_current_db()
        if db is None:
            return False, "No database selected"
    
    if not db.exist_table(table_name):
        return False, f"Table '{table_name}' does not exist"
    
    return True, db.tables[table_name]