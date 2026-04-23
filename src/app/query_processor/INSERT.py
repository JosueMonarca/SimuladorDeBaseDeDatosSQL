from src.app.controller.database import DataBase
from src.app.query_processor.USE import get_current_db

def insert(db_name: str, table_name: str, values: list) -> tuple[bool, str]:
    if db_name:
        db = DataBase.get_instance(db_name)
    else:
        db = get_current_db()
        if db is None:
            return False, "No database selected"
    
    if not db.exist_table(table_name):
        return False, f"Table '{table_name}' does not exist"
    
    parsed_values = []
    for val in values:
        try:
            if val.isdigit():
                parsed_values.append(int(val))
            elif val.replace(".", "", 1).isdigit():
                parsed_values.append(float(val))
            else:
                parsed_values.append(val)
        except:
            parsed_values.append(val)
    
    result = db.add_record(table_name, parsed_values)
    if result:
        return True, "Record inserted successfully"
    return False, "Failed to insert record"