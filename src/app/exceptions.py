class DatabaseError(Exception):
    pass

class DatabaseNotFoundError(DatabaseError):
    pass

class DatabaseAlreadyExistsError(DatabaseError):
    pass

class TableError(DatabaseError):
    pass

class TableNotFoundError(TableError):
    pass

class TableAlreadyExistsError(TableError):
    pass

class ColumnError(TableError):
    pass

class ColumnNotFoundError(ColumnError):
    pass

class RecordError(DatabaseError):
    pass

class RecordValidationError(RecordError):
    pass

class UniqueConstraintError(RecordError):
    pass

class TransactionError(DatabaseError):
    pass

class NoActiveTransactionError(TransactionError):
    pass

class AlreadyInTransactionError(TransactionError):
    pass

class PersistenceError(DatabaseError):
    pass

class FileNotFoundError(PersistenceError):
    pass

class CorruptedFileError(PersistenceError):
    pass