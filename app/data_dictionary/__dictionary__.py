from dataclasses import dataclass

@dataclass
class metadata_column:
    name: str
    unique: bool = False
    col_type : type = str 
    
@dataclass
class metadata_table:
    name: str
    columns: list[metadata_column]
    
@dataclass
class metadata_database:
    name: str
    tables: list[metadata_table]