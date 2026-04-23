from src.app.controller.database import DataBase


def insert(db_name: str, table_name: str, values: list) -> None:
    db = DataBase.get_instance(db_name)
    
    if not db.exist_table(table_name):
        from src.app.exceptions import TableNotFoundError
        raise TableNotFoundError(f"Table '{table_name}' does not exist")
    
    table = db.tables[table_name]
    col_types = [col.col_type for col in table.metadata.columns]
    
    parsed_values = []
    for i, val in enumerate(values):
        col_type = col_types[i] if i < len(col_types) else None
        
        if col_type == int:
            try:
                parsed_values.append(int(val))
            except:
                parsed_values.append(val)
        elif col_type == float:
            try:
                parsed_values.append(float(val))
            except:
                parsed_values.append(val)
        else:
            try:
                if val.isdigit():
                    parsed_values.append(int(val))
                elif val.replace(".", "", 1).replace("-", "", 1).isdigit():
                    parsed_values.append(float(val))
                else:
                    parsed_values.append(val)
            except:
                parsed_values.append(val)
    
    if not db.add_record(table_name, parsed_values):
        from src.app.exceptions import RecordValidationError
        raise RecordValidationError("Failed to insert record")