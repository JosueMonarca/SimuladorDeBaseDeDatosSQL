from app.controller.table import Table
import copy

class DataBase:
    def __init__(self):
        # Usamos un diccionario: {'nombre_tabla': objeto_tabla}
        self.tables = {}
        self.transaction_active = False
        self.backup_tables = {}

    def add_table(self, name: str) -> bool:
        if name in self.tables:
            return False
        else:
            self.tables[name] = Table(name)
            return True

    def add_column(self, table_name: str, col_name: str, col_type=None) -> bool:
        # Usamos el diccionario para acceso directo (más rápido que index)
        if table_name in self.tables:
            self.tables[table_name].add_column(col_name, col_type=col_type)
            return True
        else:
            return False

    def drop_table(self, table_name: str) -> bool:
        if table_name in self.tables:
            del self.tables[table_name]
            return True
        return False

    def all_tables(self):
        # Usamos slicing [:] para mostrar una copia de los nombres si quisiéramos
        nombres = list(self.tables.keys())
        tables = f"Tablas actuales: {nombres[:]}"
        for t in self.tables.values():
            tables += "\n" + t.to_str()
        return tables
    
    def add_record(self, table_name: str, list_of_attributes: list) ->bool:
        if self.exist_table(table_name):
            if self.tables[table_name].add_record(list_of_attributes):
                return True
        return False
    
    def exist_table(self, table_name: str) -> bool:
        return table_name in self.tables

    def begin_transaction(self):
        if not self.transaction_active:
            self.transaction_active = True
            # Create a deep copy of the current state
            self.backup_tables = copy.deepcopy(self.tables)
            return "Transaction started."
        return "Transaction already active."

    def commit_transaction(self):
        if self.transaction_active:
            self.transaction_active = False
            self.backup_tables = {}
            return "Transaction committed."
        return "No active transaction."

    def rollback_transaction(self):
        if self.transaction_active:
            self.transaction_active = False
            self.tables = self.backup_tables
            self.backup_tables = {}
            return "Transaction rolled back."
        return "No active transaction."
    
    @classmethod
    def from_dict(cls, data_dict: dict) -> 'DataBase':
        db = cls()
        
        for table_name, table_data in data_dict.items():
            db.add_table(table_name)
            for col_data in table_data["columns"]:
                # Check if it's new format (dict) or old format (str)
                if isinstance(col_data, dict):
                    col_name = col_data["name"]
                    type_str = col_data.get("type", "str")
                    col_type = int if type_str == "int" else str
                    db.add_column(table_name, col_name, col_type=col_type)
                else:
                    # Fallback for old format (list of strings)
                    db.add_column(table_name, col_data)

            for record in table_data["records"]:
                db.add_record(table_name, record)
        
        return db
    
    def to_dict(self) -> dict:
        data_dict = {}
        for table_name, table in self.tables.items():
            data_dict[table_name] = table.to_dict()
        return data_dict