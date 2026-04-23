def apply_where(records: list, columns: list, where_clause: dict) -> list:
    if not where_clause:
        return records
    
    result = []
    col_name = where_clause.get("column")
    operator = where_clause.get("operator")
    value = where_clause.get("value")
    
    col_index = None
    col_type = None
    for i, col in enumerate(columns):
        if col.name == col_name:
            col_index = i
            col_type = col.col_type
            break
    
    if col_index is None:
        return records
    
    # Convertir valor al tipo correcto
    if col_type == int:
        try:
            value = int(value)
        except:
            pass
    elif col_type == float:
        try:
            value = float(value)
        except:
            pass
    
    for record in records:
        record_value = record[col_index]
        
        try:
            if operator == "=":
                if record_value == value:
                    result.append(record)
            elif operator == "!=" or operator == "<>":
                if record_value != value:
                    result.append(record)
            elif operator == ">":
                if record_value > value:
                    result.append(record)
            elif operator == "<":
                if record_value < value:
                    result.append(record)
            elif operator == ">=":
                if record_value >= value:
                    result.append(record)
            elif operator == "<=":
                if record_value <= value:
                    result.append(record)
        except:
            pass
    
    return result