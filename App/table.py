class Table:
    """
    Clase que representa una tabla de base de datos simple.
    Permite agregar columnas, registros y validar unicidad y tipos de datos.
    """
    def __init__(self, name: str):
        """
        Inicializa una nueva instancia de Table.

        Args:
            name (str): El nombre de la tabla.
        """
        self.name = name
        self.records = [] 
        self.metadata = []

    def add_column(self, col_name: str, unique = False, type = None) -> None:
        """
        Agrega una nueva columna a la tabla.

        Args:
            col_name (str): El nombre de la columna.
            unique (bool, optional): Si la columna debe ser única. Defaults to False.
            type (type, optional): El tipo de datos esperado para la columna. Defaults to None.
        """
        if col_name not in [col[0] for col in self.metadata]:
            self.metadata.append([col_name, unique, type])
            # Actualizamos cada fila existente con un valor None para la nueva columna
            for row in self.records:
                row.append(None)
                
    """ Añade un registro a la tabla validando unicidad y tipo de datos """
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

    def to_str(self):
        """
        Convierte los registros de la tabla a una cadena de texto.

        Returns:
            str: Una cadena con cada registro en una línea.
        """
        return "\n".join([str(row) for row in self.records])