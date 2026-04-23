import copy

class TransactionManager:
    def __init__(self, db):
        self.db = db
        self.in_transaction = False
        self.original_data = None
        self.transaction_data = None

    def begin(self):
        if self.in_transaction:
            return False
        self.in_transaction = True
        self.original_data = copy.deepcopy(self.db.to_dict())
        return True

    def commit(self):
        if not self.in_transaction:
            return False
        self.in_transaction = False
        self.original_data = None
        self.transaction_data = None
        return True

    def rollback(self):
        if not self.in_transaction:
            return False
        self.db.load_from_dict(self.original_data)
        self.in_transaction = False
        self.original_data = None
        self.transaction_data = None
        return True

    def is_in_transaction(self):
        return self.in_transaction