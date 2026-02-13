import re
from app.controller.database import DataBase

def execute(db: DataBase, query: str):
    # Pattern: FROM table
    # This is usually part of SELECT/DELETE, but if invoked standalone:
    match = re.match(r"FROM\s+(\w+)", query, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        if db.exist_table(table_name):
             return f"Table '{table_name}' exists."
        else:
             return f"Table '{table_name}' does not exist."
    return "Syntax error in FROM clause."
