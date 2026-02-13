import re
from app.controller.database import DataBase
from app.query_processor.WHERE import filter_records

def execute(db: DataBase, query: str):
    # Pattern: DELETE FROM table_name [WHERE condition]
    match = re.match(r"DELETE FROM\s+(\w+)(?:\s+WHERE\s+(.+))?", query, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        condition = match.group(2)
        
        if not db.exist_table(table_name):
             return f"Error: Table '{table_name}' does not exist."
             
        table = db.tables[table_name]
        
        if condition:
            indices_to_delete = filter_records(table, condition)
            if not indices_to_delete:
                return "No records matched the condition."
            
            # Delete in reverse order to avoid index shifting issues
            for index in sorted(indices_to_delete, reverse=True):
                del table.records[index]
            return f"{len(indices_to_delete)} record(s) deleted."
        else:
            # Delete all records
            count = len(table.records)
            table.records = []
            return f"{count} record(s) deleted."
            
    return "Syntax error in DELETE command."
