from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonmRCW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onmRCW(self):
        expected = get_data(
            path='operations/onmRCWyVwCnTgsiYGGU6xUAFtuybv93d92DKxcHpc22gFJaPHK9/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onmRCWyVwCnTgsiYGGU6xUAFtuybv93d92DKxcHpc22gFJaPHK9/unsigned.json'))
        self.assertEqual(expected, actual)
