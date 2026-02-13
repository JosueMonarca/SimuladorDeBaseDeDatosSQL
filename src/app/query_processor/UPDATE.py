import re
from app.controller.database import DataBase
from app.query_processor.WHERE import filter_records

def execute(db: DataBase, query: str):
    # Pattern: UPDATE table_name SET col=val [WHERE condition]
    match = re.match(r"UPDATE\s+(\w+)\s+SET\s+(.+?)(?:\s+WHERE\s+(.+))?$", query, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        set_clause = match.group(2)
        condition = match.group(3)
        
        if not db.exist_table(table_name):
             return f"Error: Table '{table_name}' does not exist."
        
        table = db.tables[table_name]
        
        # Parse SET clause: col=val
        # Simplified: one assignment
        set_parts = set_clause.split('=')
        if len(set_parts) != 2:
             return "Syntax error in SET clause."
             
        target_col_name = set_parts[0].strip()
        target_val_str = set_parts[1].strip().strip("'").strip('"')
        
        # Find target column index and type
        target_col_idx = -1
        target_col_type = str
        for idx, col in enumerate(table.metadata.columns):
            if col.name == target_col_name:
                target_col_idx = idx
                target_col_type = col.col_type
                break
                
        if target_col_idx == -1:
            return f"Error: Column '{target_col_name}' does not exist."
            
        # Convert value
        try:
             if target_col_type == int:
                 new_value = int(target_val_str)
             else:
                 new_value = target_val_str
        except ValueError:
             return "Error: Type mismatch for update value."

        indices_to_update = []
        if condition:
            indices_to_update = filter_records(table, condition)
            if not indices_to_update:
                return "No records matched the condition."
        else:
            # Update all
            indices_to_update = range(len(table.records))
            
        for index in indices_to_update:
            table.records[index][target_col_idx] = new_value
            
        return f"{len(indices_to_update)} record(s) updated."
            
    return "Syntax error in UPDATE command."
