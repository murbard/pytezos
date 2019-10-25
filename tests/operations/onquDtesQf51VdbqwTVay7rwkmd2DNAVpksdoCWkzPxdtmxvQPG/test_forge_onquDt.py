from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonquDt(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onquDt(self):
        expected = get_data(
            path='operations/onquDtesQf51VdbqwTVay7rwkmd2DNAVpksdoCWkzPxdtmxvQPG/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onquDtesQf51VdbqwTVay7rwkmd2DNAVpksdoCWkzPxdtmxvQPG/unsigned.json'))
        self.assertEqual(expected, actual)
