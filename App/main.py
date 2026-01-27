from app.database import DataBase

db = DataBase()

db.add_table("tabla 1")
db.add_column("tabla 1", "column1")
db.add_record("tabla 1", ["column1", "column2"])
db.add_record("tabla 1", ["column1", "column2"])   
print(db.all_tables())
print(db.tables["tabla 1"])