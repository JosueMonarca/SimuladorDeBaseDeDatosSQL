from src.app.controller.database import DataBase
from src.app.transaction_manager.TransactionManager import TransactionManager
from src.app.storage_manager.PersistenceManager import PersistenceManager
from src.app import exceptions


class DBMS:
    def __init__(self):
        self.current_db = None
        self.transaction_manager = None
    
    def create_database(self, name: str) -> None:
        create_database(name)
    
    def drop_database(self, name: str) -> None:
        drop_database(name)
    
    def use_database(self, name: str) -> None:
        self.current_db = use(name)
        self.transaction_manager = TransactionManager(self.current_db)
    
    def create_table(self, table_name: str, columns: list[str]) -> None:
        if not self.current_db:
            raise exceptions.DatabaseError("No database selected")
        create_table(self.current_db.name, table_name, columns)
    
    def drop_table(self, table_name: str) -> None:
        if not self.current_db:
            raise exceptions.DatabaseError("No database selected")
        drop_table(self.current_db.name, table_name)
    
    def insert(self, table_name: str, values: list) -> None:
        if not self.current_db:
            raise exceptions.DatabaseError("No database selected")
        insert(self.current_db.name, table_name, values)
    
    def select(self, table_name: str, columns: list | None = None, where_clause: dict | None = None) -> list:
        if not self.current_db:
            raise exceptions.DatabaseError("No database selected")
        return select(self.current_db.name, table_name, columns, where_clause)
    
    def update(self, table_name: str, set_clause: dict, where_clause: dict | None = None) -> int:
        if not self.current_db:
            raise exceptions.DatabaseError("No database selected")
        return update(self.current_db.name, table_name, set_clause, where_clause)
    
    def delete(self, table_name: str, where_clause: dict | None = None) -> int:
        if not self.current_db:
            raise exceptions.DatabaseError("No database selected")
        return delete(self.current_db.name, table_name, where_clause)
    
    def alter_table(self, table_name: str, action: str, column: str | None = None) -> None:
        if not self.current_db:
            raise exceptions.DatabaseError("No database selected")
        alter_table(self.current_db.name, table_name, action, column)
    
    def begin_transaction(self) -> None:
        if not self.transaction_manager:
            raise exceptions.DatabaseError("No database selected")
        begin(self.transaction_manager)
    
    def commit_transaction(self) -> None:
        if not self.transaction_manager:
            raise exceptions.DatabaseError("No database selected")
        commit(self.transaction_manager)
    
    def rollback_transaction(self) -> None:
        if not self.transaction_manager:
            raise exceptions.DatabaseError("No database selected")
        rollback(self.transaction_manager)
    
    def is_in_transaction(self) -> bool:
        if not self.transaction_manager:
            return False
        return is_in_transaction(self.transaction_manager)
    
    def list_databases(self) -> list:
        return DataBase.list_databases()
    
    def list_tables(self) -> list:
        if not self.current_db:
            raise exceptions.DatabaseError("No database selected")
        return list(self.current_db.tables.keys())
    
    def save_db(self, filepath: str) -> None:
        if not self.current_db:
            raise exceptions.DatabaseError("No database selected")
        PersistenceManager.save_db(self.current_db, filepath)
    
    def load_db(self, filepath: str) -> None:
        db = PersistenceManager.load_db(filepath)
        loaded_db = DataBase.get_instance(db.name)
        loaded_db.tables = db.tables
        self.current_db = loaded_db
        self.transaction_manager = TransactionManager(self.current_db)

    def execute(self, query: str) -> tuple[bool, str]:
        query = query.strip()
        parts = query.upper().split()
        
        if not parts:
            return False, "Empty query"
        
        command = parts[0]
        
        try:
            if command == "CREATE_DATABASE" or command == "CREATE_DB":
                name = query.split()[1].strip(";")
                self.create_database(name)
                return True, f"Database '{name}' created successfully"
            
            elif command == "DROP_DATABASE" or command == "DROP_DB":
                name = query.split()[1].strip(";")
                self.drop_database(name)
                return True, f"Database '{name}' dropped successfully"
            
            elif command == "USE":
                name = query.split()[1].strip(";")
                self.use_database(name)
                return True, f"Using database '{name}'"
            
            elif command == "CREATE_TABLE" or command == "CREATE":
                return self._handle_create_table(query)
            
            elif command == "DROP_TABLE" or command == "DROP":
                parts = query.split()
                if len(parts) >= 3 and parts[1].upper() == "TABLE":
                    table_name = parts[2].strip(";")
                else:
                    table_name = parts[1].strip(";")
                if self.current_db:
                    self.drop_table(table_name)
                    return True, f"Table '{table_name}' dropped successfully"
                return False, "No database selected"
            
            elif command == "INSERT":
                return self._handle_insert(query)
            
            elif command == "SELECT":
                return self._handle_select(query)
            
            elif command == "UPDATE":
                return self._handle_update(query)
            
            elif command == "DELETE":
                return self._handle_delete(query)
            
            elif command == "ALTER_TABLE":
                return self._handle_alter_table(query)
            
            elif command == "BEGIN" or command == "START_TRANSACTION":
                if self.transaction_manager:
                    self.begin_transaction()
                    return True, "Transaction started"
                return False, "No database selected"
            
            elif command == "COMMIT":
                if self.transaction_manager:
                    self.commit_transaction()
                    return True, "Transaction committed"
                return False, "No database selected"
            
            elif command == "ROLLBACK":
                if self.transaction_manager:
                    self.rollback_transaction()
                    return True, "Transaction rolled back"
                return False, "No database selected"
            
            elif command == "SHOW_DATABASES":
                return True, str(self.list_databases())
            
            elif command == "SHOW_TABLES":
                if self.current_db:
                    return True, str(self.list_tables())
                return False, "No database selected"
            
            else:
                return False, f"Unknown command: {command}"
                
        except exceptions.DatabaseError as e:
            return False, f"Error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def _handle_create_table(self, query: str) -> tuple[bool, str]:
        if not self.current_db:
            return False, "No database selected"
        
        import re
        match = re.match(r'CREATE\s+TABLE\s+(\w+)\s*\((.+)\)', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            columns_str = match.group(2)
            columns = [col.strip() for col in columns_str.split(",")]
            self.create_table(table_name, columns)
            return True, f"Table '{table_name}' created successfully"
        return False, "Invalid CREATE TABLE syntax"
    
    def _handle_insert(self, query: str) -> tuple[bool, str]:
        if not self.current_db:
            return False, "No database selected"
        
        import re
        match = re.match(r'INSERT\s+INTO\s+(\w+)\s+VALUES\s*\((.+)\)', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            values_str = match.group(2)
            values = [v.strip().strip("'\"") for v in values_str.split(",")]
            self.insert(table_name, values)
            return True, "Record inserted successfully"
        return False, "Invalid INSERT syntax"
    
    def _handle_select(self, query: str) -> tuple[bool, str]:
        if not self.current_db:
            return False, "No database selected"
        
        import re
        match = re.match(r'SELECT\s+(.+?)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+))?', query, re.IGNORECASE)
        if match:
            cols_str = match.group(1).strip()
            table_name = match.group(2)
            where_str = match.group(3)
            
            columns = None if cols_str == "*" else [c.strip() for c in cols_str.split(",")]
            where_clause = self._parse_where(where_str) if where_str else None
            
            result = self.select(table_name, columns, where_clause)
            return True, str(result)
        return False, "Invalid SELECT syntax"
    
    def _handle_update(self, query: str) -> tuple[bool, str]:
        if not self.current_db:
            return False, "No database selected"
        
        import re
        match = re.match(r'UPDATE\s+(\w+)\s+SET\s+(\w+)\s*=\s*(.+?)(?:\s+WHERE\s+(.+))?$', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            col_name = match.group(2)
            value = match.group(3).strip().strip("'\"")
            where_str = match.group(4)
            
            set_clause = {"column": col_name, "value": value}
            where_clause = self._parse_where(where_str) if where_str else None
            
            count = self.update(table_name, set_clause, where_clause)
            return True, f"{count} record(s) updated"
        return False, "Invalid UPDATE syntax"
    
    def _handle_delete(self, query: str) -> tuple[bool, str]:
        if not self.current_db:
            return False, "No database selected"
        
        import re
        match = re.match(r'DELETE\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+))?$', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            where_str = match.group(2)
            
            where_clause = self._parse_where(where_str) if where_str else None
            
            count = self.delete(table_name, where_clause)
            return True, f"{count} record(s) deleted"
        return False, "Invalid DELETE syntax"
    
    def _handle_alter_table(self, query: str) -> tuple[bool, str]:
        if not self.current_db:
            return False, "No database selected"
        
        import re
        match = re.match(r'ALTER\s+TABLE\s+(\w+)\s+(ADD|DROP)\s+COLUMN\s+(\w+)', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            action = match.group(2).upper()
            column = match.group(3)
            
            self.alter_table(table_name, action, column)
            return True, f"Column '{column}' {action.lower()}ed from table '{table_name}'"
        return False, "Invalid ALTER TABLE syntax"
    
    def _parse_where(self, where_str: str) -> dict:
        import re
        match = re.match(r'(\w+)\s*(=|!=|<>|>|<|>=|<=)\s*(.+)', where_str.strip(), re.IGNORECASE)
        if match:
            col = match.group(1)
            op = match.group(2)
            val = match.group(3).strip().strip("'\"")
            return {"column": col, "operator": op, "value": val}
        raise exceptions.DatabaseError("Invalid WHERE clause")


from src.app.query_processor.CREATE_DATABASE import create_database
from src.app.query_processor.CREATE_TABLE import create_table
from src.app.query_processor.DROP_DATABASE import drop_database
from src.app.query_processor.DROP_TABLE import drop_table
from src.app.query_processor.USE import use
from src.app.query_processor.INSERT import insert
from src.app.query_processor.SELECT import select
from src.app.query_processor.UPDATE import update
from src.app.query_processor.DELETE import delete
from src.app.query_processor.ALTER_TABLE import alter_table
from src.app.transaction_manager.BEGIN import begin
from src.app.transaction_manager.COMMIT import commit
from src.app.transaction_manager.ROLLBACK import rollback
from src.app.transaction_manager.IN_TRANSACTION import is_in_transaction