from src.app.controller.database import DataBase


def insert(db_name: str, table_name: str, values: list) -> None:
    db = DataBase.get_instance(db_name)
    
    if not db.exist_table(table_name):
        from src.app.exceptions import TableNotFoundError
        raise TableNotFoundError(f"Table '{table_name}' does not exist")
    
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
    
    if not db.add_record(table_name, parsed_values):
        from src.app.exceptions import RecordValidationError
        raise RecordValidationError("Failed to insert record")