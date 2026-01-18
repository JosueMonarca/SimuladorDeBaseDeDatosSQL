from App.main import DataBase

# --- Pruebas ---
db = DataBase()
db.add_table("usuarios")
db.add_column("usuarios", "ID")
db.add_column("usuarios", "Nombre")
db.show_all_tables() # Ahora sí con paréntesis