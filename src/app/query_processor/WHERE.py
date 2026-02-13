from app.controller.table import Table

def filter_records(table: Table, condition: str) -> list[int]:
    """
    Evaluates the condition against records in the table and returns indices of matching records.
    Condition format: "col = val" (Simplified)
    Supports: =, !=, <, >, <=, >=.
    """
    indices = []
    
    # Parse condition
    # Example: "id = 1", "name = 'Alice'"
    parts = condition.split()
    if len(parts) != 3:
        return [] # Invalid or unsupported condition format
        
    col_name = parts[0]
    operator = parts[1]
    value_str = parts[2].strip("'").strip('"') # Remove quotes
    
    # Find column index and type
    col_index = -1
    col_type = str
    for idx, col in enumerate(table.metadata.columns):
        if col.name == col_name:
            col_index = idx
            col_type = col.col_type
            break
            
    if col_index == -1:
        return [] # Column not found
        
    # Convert value to correct type
    try:
        if col_type == int:
            value = int(value_str)
        else:
            value = value_str
    except ValueError:
        return [] # Type mismatch
        
    for index, record in enumerate(table.records):
        cell_value = record[col_index]
        
        match = False
        if operator == '=':
            match = cell_value == value
        elif operator == '!=':
            match = cell_value != value
        elif operator == '<':
            match = cell_value < value
        elif operator == '>':
            match = cell_value > value
        elif operator == '<=':
            match = cell_value <= value
        elif operator == '>=':
            match = cell_value >= value
            
        if match:
            indices.append(index)
            
    return indices
