from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonezot(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onezot(self):
        expected = get_data(
            path='operations/onezotpHPjfcBCWxTtgUHWXoyrFTkDerMiyY5XVKqvZssofG8Hm/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onezotpHPjfcBCWxTtgUHWXoyrFTkDerMiyY5XVKqvZssofG8Hm/unsigned.json'))
        self.assertEqual(expected, actual)
