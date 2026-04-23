from src.app.transaction_manager.TransactionManager import TransactionManager

def is_in_transaction(tm: TransactionManager):
    return tm.is_in_transaction()