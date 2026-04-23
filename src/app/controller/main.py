from src.app.controller.database import DataBase
from src.app.controller.table import Table
from src.app.transaction_manager.TransactionManager import TransactionManager
from src.app.storage_manager.PersistenceManager import PersistenceManager

from src.app.query_processor.CREATE_DATABASE import create_database
from src.app.query_processor.CREATE_TABLE import create_table
from src.app.query_processor.DROP_DATABASE import drop_database
from src.app.query_processor.DROP_TABLE import drop_table
from src.app.query_processor.USE import use, get_current_db
from src.app.query_processor.INSERT import insert
from src.app.query_processor.SELECT import select
from src.app.query_processor.UPDATE import update
from src.app.query_processor.DELETE import delete
from src.app.query_processor.ALTER_TABLE import alter_table

from src.app.transaction_manager.BEGIN import begin
from src.app.transaction_manager.COMMIT import commit
from src.app.transaction_manager.ROLLBACK import rollback
from src.app.transaction_manager.IN_TRANSACTION import is_in_transaction


class DBMS:
    def __init__(self):
        self.databases = {}
        self.current_db = None
        self.transaction_manager = None
    
    def execute(self, query: str) -> tuple[bool, str]:
        query = query.strip()
        parts = query.upper().split()
        
        if not parts:
            return False, "Empty query"
        
        command = parts[0]
        
        try:
            if command == "CREATE_DATABASE" or command == "CREATE_DB":
                name = query.split()[1].strip(";")
                return create_database(name)
            
            elif command == "DROP_DATABASE" or command == "DROP_DB":
                name = query.split()[1].strip(";")
                return drop_database(name)
            
            elif command == "USE":
                name = query.split()[1].strip(";")
                success, msg = use(name)
                if success:
                    self.current_db = get_current_db()
                    self.transaction_manager = TransactionManager(self.current_db)
                return success, msg
            
            elif command == "CREATE_TABLE" or command == "CREATE":
                return self._handle_create_table(query)
            
            elif command == "DROP_TABLE" or command == "DROP":
                parts = query.split()
                if len(parts) >= 3 and parts[1].upper() == "TABLE":
                    table_name = parts[2].strip(";")
                else:
                    table_name = parts[1].strip(";")
                if self.current_db:
                    return drop_table(self.current_db.name, table_name)
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
                    return begin(self.transaction_manager)
                return False, "No database selected"
            
            elif command == "COMMIT":
                if self.transaction_manager:
                    return commit(self.transaction_manager)
                return False, "No database selected"
            
            elif command == "ROLLBACK":
                if self.transaction_manager:
                    return rollback(self.transaction_manager)
                return False, "No database selected"
            
            elif command == "SHOW_DATABASES":
                return True, DataBase.list_databases()
            
            elif command == "SHOW_TABLES":
                if self.current_db:
                    return True, list(self.current_db.tables.keys())
                return False, "No database selected"
            
            else:
                return False, f"Unknown command: {command}"
                
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
            return create_table(self.current_db.name, table_name, columns)
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
            return insert(self.current_db.name, table_name, values)
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
            
            return select(self.current_db.name, table_name, columns, where_clause)
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
            
            return update(self.current_db.name, table_name, set_clause, where_clause)
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
            
            return delete(self.current_db.name, table_name, where_clause)
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
            
            return alter_table(self.current_db.name, table_name, action, column)
        return False, "Invalid ALTER TABLE syntax"
    
    def _parse_where(self, where_str: str) -> dict:
        import re
        match = re.match(r'(\w+)\s*(=|!=|<>|>|<|>=|<=)\s*(.+)', where_str.strip(), re.IGNORECASE)
        if match:
            col = match.group(1)
            op = match.group(2)
            val = match.group(3).strip().strip("'\"")
            return {"column": col, "operator": op, "value": val}
        return None
    
    def save_db(self, filepath: str):
        if self.current_db:
            PersistenceManager.save_db(self.current_db, filepath)
            return True
        return False
    
    def load_db(self, filepath: str):
        db = PersistenceManager.load_db(filepath)
        DataBase.get_instance(db.name)
        return db


def main():
    dbms = DBMS()
    
    print("=== Simulador de Base de Datos ===")
    print("Comandos: CREATE_DATABASE, USE, CREATE_TABLE, INSERT, SELECT, UPDATE, DELETE, etc.")
    print("Escribe 'exit' para salir\n")
    
    while True:
        try:
            query = input("db> ").strip()
            if query.lower() in ("exit", "quit"):
                break
            
            if query:
                success, result = dbms.execute(query)
                if success:
                    print(result)
                else:
                    print(f"Error: {result}")
                    
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()