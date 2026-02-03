from dataclasses import dataclass

@dataclass
class metadata:
    col_name: str
    unique: bool = False
    type : type = str 