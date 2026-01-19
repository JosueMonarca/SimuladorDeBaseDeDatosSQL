from App.table import Table

class DataBase:
    def __init__(self):
        # Usamos un diccionario: {'nombre_tabla': objeto_tabla}
        self.tables = {}

    def add_table(self, name: str) -> bool:
        # Aplicando OPERADOR TERNARIO para validar existencia
        if name in self.tables:
            return False
        else:
            self.tables[name] = Table(name)
            return True

    def add_column(self, table_name, col_name) -> bool:
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