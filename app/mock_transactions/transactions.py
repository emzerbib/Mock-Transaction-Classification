import random
from .columns import Columns



PARAMETER_DICT = {
        Columns.CLIENT: {
            Columns.AMOUNT_RANGE: (15, 780),
            Columns.TAG_CHOICES: ('delivery', 'bulk purchase', 'G_dist'),
            Columns.HOUR_RANGE: (10, 18)
            },
        Columns.SUPPLIER: {
            Columns.AMOUNT_RANGE: (2400, 18000),
            Columns.TAG_CHOICES: ('ABC_inc', 'XYZ_inc', 'AAA_&_BBB'),
            Columns.HOUR_RANGE: (6, 21)
            },
        Columns.TAX: {
            Columns.AMOUNT_RANGE: (900, 35000),
            Columns.TAG_CHOICES: ('CPAM', 'ARC', 'RevenuQc'),
            Columns.HOUR_RANGE: (0, 1)
            }
            }

class Transaction():

    __parameter_dict = PARAMETER_DICT
    
    def __init__(self, amount: int, tag: str, hour: int) -> None:
        self._amount = amount,
        self._tag = tag,
        self._hour = hour,

    @classmethod
    def get_class_parameter_dict(cls):
        return cls.__parameter_dict

    def get_dict(self):
        return {
            Columns.AMOUNT: self._amount,
            Columns.TAG: self._tag,
            Columns.HOUR: self._hour,
        }

class GenericTransaction(Transaction):
    def __init__(self, transaction_type: str):
        self._type = transaction_type
        self._amount_range = self.get_class_parameter_dict()[self._type][Columns.AMOUNT_RANGE]
        self._tag_choices =  self.get_class_parameter_dict()[self._type][Columns.TAG_CHOICES]
        self._hour_range =  self.get_class_parameter_dict()[self._type][Columns.HOUR_RANGE]
        self._amount = random.randint(*self._amount_range)
        self._tag = random.choice(self._tag_choices)
        self._hour = random.randint(*self._hour_range)