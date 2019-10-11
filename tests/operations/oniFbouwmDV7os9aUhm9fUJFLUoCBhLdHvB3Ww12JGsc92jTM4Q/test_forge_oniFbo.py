from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoniFbo(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oniFbo(self):
        expected = get_data(
            path='operations/oniFbouwmDV7os9aUhm9fUJFLUoCBhLdHvB3Ww12JGsc92jTM4Q/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oniFbouwmDV7os9aUhm9fUJFLUoCBhLdHvB3Ww12JGsc92jTM4Q/unsigned.json'))
        self.assertEqual(expected, actual)
