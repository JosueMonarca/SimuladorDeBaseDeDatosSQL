from App.table import Table

class DataBase:
    def __init__(self):
        # Usamos un diccionario: {'nombre_tabla': objeto_tabla}
        self.tables = {}

    def add_table(self, name):
        # Aplicando OPERADOR TERNARIO para validar existencia
        if name in self.tables:
            print(f"La tabla '{name}' ya existe.")
        else:
            self.tables[name] = Table(name)

    def add_column(self, table_name, col_name):
        # Usamos el diccionario para acceso directo (más rápido que index)
        if table_name in self.tables:
            self.tables[table_name].add_column(col_name)
        else:
            print("Error: La tabla no existe.")

    def show_all_tables(self):
        # Usamos slicing [:] para mostrar una copia de los nombres si quisiéramos
        nombres = list(self.tables.keys())
        print(f"Tablas actuales: {nombres[:]}") 
        for t in self.tables.values():
            print(t.to_str())

