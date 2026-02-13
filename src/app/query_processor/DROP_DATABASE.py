import re
import os
from app.controller.database import DataBase

def execute(db: DataBase, query: str):
    # Pattern: DROP DATABASE db_name
    match = re.match(r"DROP DATABASE\s+(.+)", query, re.IGNORECASE)
    if match:
        db_name = match.group(1).strip()
        filepath = f"{db_name}.json"
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return f"Database '{db_name}' dropped successfully."
            except Exception as e:
                return f"Error dropping database: {e}"
        else:
            return f"Error: Database '{db_name}' does not exist."
            
    return "Syntax error in DROP DATABASE command."
