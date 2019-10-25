from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooh3DW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooh3DW(self):
        expected = get_data(
            path='operations/ooh3DWWtdLYqKnV5BNfFGArwrBiuZc5tGkmFLv5qgGGkabCAwAa/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooh3DWWtdLYqKnV5BNfFGArwrBiuZc5tGkmFLv5qgGGkabCAwAa/unsigned.json'))
        self.assertEqual(expected, actual)
