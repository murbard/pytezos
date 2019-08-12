from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooMPrF(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooMPrF(self):
        expected = get_data(
            path='operations/ooMPrF3bhW8pnEYFeLk36Y9k2yy8UwLKjvfd1ZF1sPP4bY1sbsi/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooMPrF3bhW8pnEYFeLk36Y9k2yy8UwLKjvfd1ZF1sPP4bY1sbsi/unsigned.json'))
        self.assertEqual(expected, actual)
