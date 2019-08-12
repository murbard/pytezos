from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopUcue(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opUcue(self):
        expected = get_data(
            path='operations/opUcuepQjxETNLLi29M5c1VW4Ji13oGA5tzAup1wsC2RfvWnVGD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opUcuepQjxETNLLi29M5c1VW4Ji13oGA5tzAup1wsC2RfvWnVGD/unsigned.json'))
        self.assertEqual(expected, actual)
