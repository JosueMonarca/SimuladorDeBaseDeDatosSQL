from src.app.transaction_manager.TransactionManager import TransactionManager

def commit(tm: TransactionManager):
    result = tm.commit()
    return result, "Transaction committed" if result else "No active transaction"