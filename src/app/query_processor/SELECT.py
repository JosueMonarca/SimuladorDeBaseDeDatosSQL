import re
from app.controller.database import DataBase

def execute(db: DataBase, query: str):
    # Pattern: SELECT * FROM table_name
    match = re.match(r"SELECT\s+\*\s+FROM\s+(\w+)", query, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        if db.exist_table(table_name):
            table = db.tables[table_name]
            return table.to_str()
        else:
            return f"Error: Table '{table_name}' does not exist."
    return "Syntax error in SELECT command or feature not supported (only SELECT * FROM table is supported)."
