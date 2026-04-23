from src.app.service.dbms_service import DBMS
from src.app import exceptions


class CLI:
    def __init__(self):
        self.dbms = DBMS()
    
    def execute(self, query: str) -> str:
        query = query.strip()
        if not query:
            return "Empty query"
        
        parts = query.upper().split()
        command = parts[0]
        
        try:
            if command == "CREATE_DATABASE" or command == "CREATE_DB":
                name = query.split()[1].strip(";")
                self.dbms.create_database(name)
                return f"Database '{name}' created successfully"
            
            elif command == "DROP_DATABASE" or command == "DROP_DB":
                name = query.split()[1].strip(";")
                self.dbms.drop_database(name)
                return f"Database '{name}' dropped successfully"
            
            elif command == "USE":
                name = query.split()[1].strip(";")
                self.dbms.use_database(name)
                return f"Using database '{name}'"
            
            elif command == "CREATE_TABLE" or command == "CREATE":
                return self._handle_create_table(query)
            
            elif command == "DROP_TABLE" or command == "DROP":
                return self._handle_drop_table(query)
            
            elif command == "INSERT":
                return self._handle_insert(query)
            
            elif command == "SELECT":
                return self._handle_select(query)
            
            elif command == "UPDATE":
                return self._handle_update(query)
            
            elif command == "DELETE":
                return self._handle_delete(query)
            
            elif command == "ALTER_TABLE" or command == "ALTER":
                return self._handle_alter_table(query)
            
            elif command == "BEGIN" or command == "START_TRANSACTION":
                self.dbms.begin_transaction()
                return "Transaction started"
            
            elif command == "COMMIT":
                self.dbms.commit_transaction()
                return "Transaction committed"
            
            elif command == "ROLLBACK":
                self.dbms.rollback_transaction()
                return "Transaction rolled back"
            
            elif command == "SHOW_DATABASES":
                return str(self.dbms.list_databases())
            
            elif command == "SHOW_TABLES":
                return str(self.dbms.list_tables())
            
            elif command == "SAVE_DB":
                parts = query.split()
                if len(parts) >= 2:
                    filepath = parts[1].strip(";")
                    self.dbms.save_db(filepath)
                    return f"Database saved to '{filepath}'"
                return "Usage: SAVE_DB "
            
            elif command == "LOAD_DB":
                parts = query.split()
                if len(parts) >= 2:
                    filepath = parts[1].strip(";")
                    self.dbms.load_db(filepath)
                    if self.dbms.current_db:
                        self.dbms.use_database(self.dbms.current_db.name)
                    return f"Database loaded from '{filepath}'"
                return "Usage: LOAD_DB "
            
            else:
                return f"Unknown command: {command}"
                
        except exceptions.DatabaseError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _handle_create_table(self, query: str) -> str:
        import re
        match = re.match(r'CREATE\s+TABLE\s+(\w+)\s*\((.+)\)', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            columns_str = match.group(2)
            columns = [col.strip() for col in columns_str.split(",")]
            self.dbms.create_table(table_name, columns)
            return f"Table '{table_name}' created successfully"
        return "Invalid CREATE TABLE syntax"
    
    def _handle_drop_table(self, query: str) -> str:
        parts = query.split()
        if len(parts) >= 3 and parts[1].upper() == "TABLE":
            table_name = parts[2].strip(";")
        else:
            table_name = parts[1].strip(";")
        self.dbms.drop_table(table_name)
        return f"Table '{table_name}' dropped successfully"
    
    def _handle_insert(self, query: str) -> str:
        import re
        match = re.match(r'INSERT\s+INTO\s+(\w+)\s+VALUES\s*\((.+)\)', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            values_str = match.group(2)
            values = [v.strip().strip("'\"") for v in values_str.split(",")]
            self.dbms.insert(table_name, values)
            return "Record inserted successfully"
        return "Invalid INSERT syntax"
    
    def _handle_select(self, query: str) -> str:
        import re
        match = re.match(r'SELECT\s+(.+?)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+))?', query, re.IGNORECASE)
        if match:
            cols_str = match.group(1).strip()
            table_name = match.group(2)
            where_str = match.group(3)
            
            columns = None if cols_str == "*" else [c.strip() for c in cols_str.split(",")]
            where_clause = self._parse_where(where_str) if where_str else None
            
            result = self.dbms.select(table_name, columns, where_clause)
            return str(result)
        return "Invalid SELECT syntax"
    
    def _handle_update(self, query: str) -> str:
        import re
        match = re.match(r'UPDATE\s+(\w+)\s+SET\s+(\w+)\s*=\s*(.+?)(?:\s+WHERE\s+(.+))?$', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            col_name = match.group(2)
            value = match.group(3).strip().strip("'\"")
            where_str = match.group(4)
            
            set_clause = {"column": col_name, "value": value}
            where_clause = self._parse_where(where_str) if where_str else None
            
            count = self.dbms.update(table_name, set_clause, where_clause)
            return f"{count} record(s) updated"
        return "Invalid UPDATE syntax"
    
    def _handle_delete(self, query: str) -> str:
        import re
        match = re.match(r'DELETE\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+))?$', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            where_str = match.group(2)
            
            where_clause = self._parse_where(where_str) if where_str else None
            
            count = self.dbms.delete(table_name, where_clause)
            return f"{count} record(s) deleted"
        return "Invalid DELETE syntax"
    
    def _handle_alter_table(self, query: str) -> str:
        import re
        match = re.match(r'ALTER\s+TABLE\s+(\w+)\s+(ADD|DROP)\s+COLUMN\s+(\w+)', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            action = match.group(2).upper()
            column = match.group(3)
            
            self.dbms.alter_table(table_name, action, column)
            return f"Column '{column}' added to table '{table_name}'"
        return "Invalid ALTER TABLE syntax"
    
    def _parse_where(self, where_str: str) -> dict:
        import re
        # Manejar >= y <= primero
        match = re.match(r'(\w+)\s*>=\s*(.+)', where_str.strip(), re.IGNORECASE)
        if match:
            col = match.group(1)
            val = match.group(2).strip().strip("'\"")
            return {"column": col, "operator": ">=", "value": val}
        
        match = re.match(r'(\w+)\s*<=\s*(.+)', where_str.strip(), re.IGNORECASE)
        if match:
            col = match.group(1)
            val = match.group(2).strip().strip("'\"")
            return {"column": col, "operator": "<=", "value": val}
        
        match = re.match(r'(\w+)\s*(!=|<>)\s*(.+)', where_str.strip(), re.IGNORECASE)
        if match:
            col = match.group(1)
            val = match.group(3).strip().strip("'\"")
            return {"column": col, "operator": match.group(2), "value": val}
        
        match = re.match(r'(\w+)\s*>\s*(.+)', where_str.strip(), re.IGNORECASE)
        if match:
            col = match.group(1)
            val = match.group(2).strip().strip("'\"")
            return {"column": col, "operator": ">", "value": val}
        
        match = re.match(r'(\w+)\s*<\s*(.+)', where_str.strip(), re.IGNORECASE)
        if match:
            col = match.group(1)
            val = match.group(2).strip().strip("'\"")
            return {"column": col, "operator": "<", "value": val}
        
        match = re.match(r'(\w+)\s*=\s*(.+)', where_str.strip(), re.IGNORECASE)
        if match:
            col = match.group(1)
            val = match.group(2).strip().strip("'\"")
            return {"column": col, "operator": "=", "value": val}
        
        return None
    
    def run(self):
        print("=== Simulador de Base de Datos ===")
        print("Comandos: CREATE_DATABASE, USE, CREATE_TABLE, INSERT, SELECT, etc.")
        print("Escribe 'exit' para salir\n")
        
        while True:
            try:
                query = input("db> ").strip()
                if query.lower() in ("exit", "quit"):
                    break
                
                if query:
                    print(self.execute(query))
                    
            except KeyboardInterrupt:
                print("\nSaliendo...")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    cli = CLI()
    cli.run()