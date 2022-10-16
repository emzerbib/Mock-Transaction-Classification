from .columns import Columns
from .transactions import GenericTransaction
import random

def generate_random_transactions(n: int, proportions: tuple = (.94,.05,.01)):
    """
    generate n mock transaction with proportions (c, s, t) where:
    c is the percentage of client transaction
    s is the percentage of supplier transaction
    t is the percentage of tax transaction

    """
    if sum(proportions) != 1:
        raise InvalidTuple(proportions=proportions)
    
    c, s, t = (round(p*n) for p in proportions)

    client_transactions = [GenericTransaction(transaction_type=Columns.CLIENT) for n in range(c)]
    supplier_transactions = [GenericTransaction(transaction_type=Columns.SUPPLIER) for n in range(s)]
    tax_transactions = [GenericTransaction(transaction_type=Columns.TAX) for n in range(t)]

    transactions = client_transactions + supplier_transactions + tax_transactions
    
    random.shuffle(transactions)

    return transactions