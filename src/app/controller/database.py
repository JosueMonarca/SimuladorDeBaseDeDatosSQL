from app.controller.table import Table

class DataBase:
    def __init__(self):
        # Usamos un diccionario: {'nombre_tabla': objeto_tabla}
        self.tables = {}

    def add_table(self, name: str) -> bool:
        if name in self.tables:
            return False
        else:
            self.tables[name] = Table(name)
            return True

    def add_column(self, table_name: str, col_name: str) -> bool:
        # Usamos el diccionario para acceso directo (más rápido que index)
        if table_name in self.tables:
            self.tables[table_name].add_column(col_name)
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
        db = cls()
        
        for table_name, table_data in data_dict.items():
            db.add_table(table_name)
            for col_name in table_data["columns"]:
                db.add_column(table_name, col_name)
            for record in table_data["records"]:
                db.add_record(table_name, record)
        
        return db
    
    def to_dict(self) -> dict:
        data_dict = {}
        for table_name, table in self.tables.items():
            data_dict[table_name] = table.to_dict()
        return data_dict