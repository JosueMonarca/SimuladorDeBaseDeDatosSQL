from app.data_dictionary.__dictionary__ import metadata_column
from app.data_dictionary.__dictionary__ import metadata_table
class Table:
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.records = [] 
        self.metadata = metadata_table(name, [])

    def add_column(self, col_name: str, unique = False, col_type = None) -> None:
        if col_name not in [col.name for col in self.metadata.columns]:
            self.metadata.columns.append(metadata_column(col_name, unique, col_type = col_type if col_type else str))
            for row in self.records:
                row.append(None)
                
    def add_record(self, record: list) -> bool:
        auxiliary_registration = []
        
        if(len(record) == len(self.metadata.columns)):
            counter = 0
            for item in record:
                if self.metadata.columns[counter].unique:  # Si es único
                    if item in [row[counter] for row in self.records]:
                        return False
                if self.metadata.columns[counter].col_type is not None:  # Si hay un tipo definido
                    if not isinstance(item, self.metadata.columns[counter].col_type):
                        return False
                auxiliary_registration.append(item)
                counter += 1
            self.records.append(auxiliary_registration)
        else:
            return False
        return True
    
    def to_dict(self) -> dict:
        return {
            "columns": [col.name for col in self.metadata.columns],
            "records": self.records
        }

    def to_str(self):
        return "\n".join([str(row) for row in self.records])