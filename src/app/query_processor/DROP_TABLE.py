import re
from app.controller.database import DataBase

def execute(db: DataBase, query: str):
    # Pattern: DROP TABLE table_name
    match = re.match(r"DROP TABLE\s+(\w+)", query, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        if db.drop_table(table_name):
            return f"Table '{table_name}' dropped successfully."
        else:
            return f"Error: Table '{table_name}' does not exist."
    return "Syntax error in DROP TABLE command."
