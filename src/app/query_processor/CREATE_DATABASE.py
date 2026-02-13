import re
import os
import json
from app.controller.database import DataBase

def execute(db: DataBase, query: str):
    # Pattern: CREATE DATABASE db_name
    match = re.match(r"CREATE DATABASE\s+(.+)", query, re.IGNORECASE)
    if match:
        db_name = match.group(1).strip()
        filepath = f"{db_name}.json"
        
        if os.path.exists(filepath):
            return f"Error: Database '{db_name}' already exists."
        
        # Create empty db file
        try:
            with open(filepath, 'w') as f:
                json.dump({}, f)
            return f"Database '{db_name}' created successfully."
        except Exception as e:
            return f"Error creating database: {e}"
            
    return "Syntax error in CREATE DATABASE command."
