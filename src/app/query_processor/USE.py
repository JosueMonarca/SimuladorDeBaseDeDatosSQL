import re
import os
from app.controller.database import DataBase
from app.storage_manager.persistence_manager import PersistenceManager

def execute(db: DataBase, query: str):
    # Pattern: USE db_name
    match = re.match(r"USE\s+(.+)", query, re.IGNORECASE)
    if match:
        db_name = match.group(1).strip()
        # simplified: assuming db_name corresponds to db_name.json
        filepath = f"{db_name}.json" 
        
        if not os.path.exists(filepath):
            return f"Error: Database '{db_name}' does not exist."
            
        try:
            new_db = PersistenceManager.load_db(filepath)
            # Switch context
            db.tables = new_db.tables
            db.transaction_active = False 
            db.backup_tables = {}
            return f"Switched to database '{db_name}'."
        except Exception as e:
            return f"Error switching database: {e}"
            
    return "Syntax error in USE command."
