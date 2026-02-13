import re
from app.controller.database import DataBase

def execute(db: DataBase, query: str):
    # Pattern: ALTER TABLE table_name ADD column_name type
    # Simplified: ALTER TABLE table_name ADD column_name [type]
    match = re.match(r"ALTER TABLE\s+(\w+)\s+ADD\s+(\w+)(?:\s+(\w+))?", query, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        col_name = match.group(2)
        type_str = match.group(3)
        
        if not db.exist_table(table_name):
            return f"Error: Table '{table_name}' does not exist."
            
        col_type = str # Default
        if type_str:
            if type_str.lower() == 'int':
                col_type = int
            elif type_str.lower() == 'str':
                col_type = str
        
        if db.add_column(table_name, col_name, col_type=col_type):
            return f"Table '{table_name}' altered successfully. Column '{col_name}' added."
        else:
            # Should not happen if exist_table check passed, unless column already exists check is failing or returns False
            # db.add_column returns False if table doesn't exist, but we checked.
            # However, table.add_column doesn't return anything.
            # Wait, app/controller/database.py returns True if table exists.
            # But table.add_column logic: if col_name not in metadata... append.
            # It doesn't return success/fail on column existence.
            return f"Column '{col_name}' added to '{table_name}'."
            
    return "Syntax error in ALTER TABLE command."
