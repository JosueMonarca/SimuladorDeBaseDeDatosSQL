from src.app.controller.table import Table

class DataBase:
    _instances = {}
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.tables = {}

    @classmethod
    def get_instance(cls, name: str = "default") -> 'DataBase':
        if name not in cls._instances:
            cls._instances[name] = cls(name)
        return cls._instances[name]

    @classmethod
    def remove_instance(cls, name: str) -> bool:
        if name in cls._instances:
            del cls._instances[name]
            return True
        return False
    
    @classmethod
    def exists(cls, name: str) -> bool:
        return name in cls._instances

    @classmethod
    def list_databases(cls) -> list:
        return list(cls._instances.keys())

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
    
    @classmethod
    def from_dict(cls, data_dict: dict) -> DataBase:
        db = DataBase.get_instance("default")
        
        for table_name, table_data in data_dict.items():
            db.add_table(table_name)
            for col_name in table_data["columns"]:
                db.add_column(table_name, col_name)
            for record in table_data["records"]:
                db.add_record(table_name, record)
        
        return db
    
    def load_from_dict(self, data_dict: dict) -> None:
        self.tables = {}
        for table_name, table_data in data_dict.items():
            self.add_table(table_name)
            for col_name in table_data["columns"]:
                self.add_column(table_name, col_name)
            for record in table_data["records"]:
                self.add_record(table_name, record)
    
    def to_dict(self) -> dict:
        data_dict = {}
        for table_name, table in self.tables.items():
            data_dict[table_name] = table.to_dict()
        return data_dict