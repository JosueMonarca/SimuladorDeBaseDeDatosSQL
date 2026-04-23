from src.app.transaction_manager.TransactionManager import TransactionManager

def begin(tm: TransactionManager):
    result = tm.begin()
    return result, "Transaction started" if result else "Already in transaction"