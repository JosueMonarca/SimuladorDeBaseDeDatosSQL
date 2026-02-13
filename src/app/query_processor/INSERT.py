import re
from app.controller.database import DataBase

def execute(db: DataBase, query: str):
    # Pattern: INSERT INTO table_name VALUES (val1, val2, ...)
    match = re.match(r"INSERT INTO\s+(\w+)\s+VALUES\s*\((.+)\)", query, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        values_str = match.group(2)
        
        # Split values by comma, handling potential quotes (simplified)
        # Using a simple split for now, robust parsing would handle commas in strings
        values = [v.strip().strip("'").strip('"') for v in values_str.split(',')]
        
        # Convert to appropriate types if possible (basic int conversion)
        parsed_values = []
        for v in values:
            if v.isdigit():
                parsed_values.append(int(v))
            else:
                parsed_values.append(v)
        
        if db.exist_table(table_name):
            if db.add_record(table_name, parsed_values):
                return "Record inserted successfully."
            else:
                return "Error: Failed to insert record (constraint violation or type mismatch)."
        else:
            return f"Error: Table '{table_name}' does not exist."
    return "Syntax error in INSERT command."
