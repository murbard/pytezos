from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooXLzr(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooXLzr(self):
        expected = get_data(
            path='operations/ooXLzrWeQJe4ZsN4nPh3RsNzjFEr3JpCzFy9fegvRAgHTjm4vSc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooXLzrWeQJe4ZsN4nPh3RsNzjFEr3JpCzFy9fegvRAgHTjm4vSc/unsigned.json'))
        self.assertEqual(expected, actual)
