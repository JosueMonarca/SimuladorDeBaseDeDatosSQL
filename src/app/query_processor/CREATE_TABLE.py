import re
from app.controller.database import DataBase

def execute(db: DataBase, query: str):
    # Pattern: CREATE TABLE table_name (col1 type1, col2 type2, ...)
    match = re.match(r"CREATE TABLE\s+(\w+)\s*\((.+)\)", query, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        columns_def = match.group(2)
        
        if db.add_table(table_name):
            # Parse columns
            # Example: id int, name str
            columns = [c.strip() for c in columns_def.split(',')]
            for col in columns:
                # Simplified parsing: assume "name type" or just "name"
                parts = col.split()
                col_name = parts[0]
                col_type = str # Default
                
                if len(parts) > 1:
                    type_str = parts[1].lower()
                    if type_str == 'int':
                        col_type = int
                    elif type_str == 'str':
                        col_type = str
                        
                db.add_column(table_name, col_name, col_type=col_type) # Create table with types? Wait, add_column doesn't take type in `database.py` wrapper?
            return f"Table '{table_name}' created successfully."
        else:
            return f"Error: Table '{table_name}' already exists."
    return "Syntax error in CREATE TABLE command."
