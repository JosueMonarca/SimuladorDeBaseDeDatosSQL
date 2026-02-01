class Table:
    
    def __init__(self, name: str):
        
        self.name = name
        self.records = [] 
        self.metadata = []

    def add_column(self, col_name: str, unique = False, type = None) -> None:
        if col_name not in [col[0] for col in self.metadata]:
            self.metadata.append([col_name, unique, type])
            for row in self.records:
                row.append(None)
                
    def add_record(self, record: list) -> bool:
        auxiliary_registration = []
        
        if(len(record) == len(self.metadata)):
            counter = 0
            for item in record:
                if self.metadata[counter][1]:  # Si es único
                    if item in [row[counter] for row in self.records]:
                        return False
                if self.metadata[counter][2] is not None:  # Si hay un tipo definido
                    if not isinstance(item, self.metadata[counter][2]):
                        return False
                auxiliary_registration.append(item)
                counter += 1
            self.records.append(auxiliary_registration)
        else:
            return False
        return True
    
    def to_dict(self) -> dict:
        return {
            "columns": [col[0] for col in self.metadata],
            "records": self.records
        }

    def to_str(self):
        return "\n".join([str(row) for row in self.records])