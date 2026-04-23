from src.app.transaction_manager.TransactionManager import TransactionManager

def rollback(tm: TransactionManager):
    result = tm.rollback()
    return result, "Transaction rolled back" if result else "No active transaction"