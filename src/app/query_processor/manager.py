import re
from app.controller.database import DataBase
from app.transaction_manager import BEGIN, COMMIT, ROLLBACK
from app.query_processor import CREATE_TABLE, INSERT, SELECT, DELETE, UPDATE, DROP_TABLE, ALTER_TABLE, CREATE_DATABASE, DROP_DATABASE, USE, FROM
from app.storage_manager.persistence_manager import PersistenceManager

class QueryProcessor:
    def __init__(self, db: DataBase):
        self.db = db

    def execute(self, query: str):
        query = query.strip()
        
        # Transaction Commands
        if re.match(r"^BEGIN TRANSACTION$", query, re.IGNORECASE):
            return BEGIN.execute(self.db)
        elif re.match(r"^COMMIT TRANSACTION$", query, re.IGNORECASE):
            return COMMIT.execute(self.db)
        elif re.match(r"^ROLLBACK TRANSACTION$", query, re.IGNORECASE):
            return ROLLBACK.execute(self.db)
            
        # Storage Manager / Database Commands
        match_save = re.match(r"^SAVE DATABASE\s+(.+)$", query, re.IGNORECASE)
        if match_save:
            filepath = match_save.group(1).strip()
            # ... (existing logic) ...
            try:
                PersistenceManager.save_db(self.db, filepath)
                return f"Database saved to {filepath}"
            except Exception as e:
                return f"Error saving database: {e}"

        match_load = re.match(r"^LOAD DATABASE\s+(.+)$", query, re.IGNORECASE)
        if match_load:
            # ... (existing logic) ...
            filepath = match_load.group(1).strip()
            try:
                new_db = PersistenceManager.load_db(filepath)
                self.db.tables = new_db.tables
                self.db.transaction_active = False
                self.db.backup_tables = {}
                return f"Database loaded from {filepath}"
            except Exception as e:
                return f"Error loading database: {e}"

        if re.match(r"^CREATE DATABASE", query, re.IGNORECASE):
            return CREATE_DATABASE.execute(self.db, query)
        elif re.match(r"^DROP DATABASE", query, re.IGNORECASE):
            return DROP_DATABASE.execute(self.db, query)
        elif re.match(r"^USE", query, re.IGNORECASE):
            return USE.execute(self.db, query)
            
        # DDL Commands
        elif re.match(r"^CREATE TABLE", query, re.IGNORECASE):
            return CREATE_TABLE.execute(self.db, query)
        elif re.match(r"^DROP TABLE", query, re.IGNORECASE):
            return DROP_TABLE.execute(self.db, query)
        elif re.match(r"^ALTER TABLE", query, re.IGNORECASE):
            return ALTER_TABLE.execute(self.db, query)
            
        # DML Commands
        elif re.match(r"^INSERT INTO", query, re.IGNORECASE):
            return INSERT.execute(self.db, query)
        elif re.match(r"^SELECT", query, re.IGNORECASE):
            return SELECT.execute(self.db, query)
        elif re.match(r"^DELETE FROM", query, re.IGNORECASE):
            return DELETE.execute(self.db, query)
        elif re.match(r"^UPDATE", query, re.IGNORECASE):
            return UPDATE.execute(self.db, query)
        elif re.match(r"^FROM", query, re.IGNORECASE):
            return FROM.execute(self.db, query)
            
        return "Unknown command or syntax error."
