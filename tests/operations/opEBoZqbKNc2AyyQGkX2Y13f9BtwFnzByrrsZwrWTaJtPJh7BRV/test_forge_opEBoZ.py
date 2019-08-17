from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopEBoZ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opEBoZ(self):
        expected = get_data(
            path='operations/opEBoZqbKNc2AyyQGkX2Y13f9BtwFnzByrrsZwrWTaJtPJh7BRV/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opEBoZqbKNc2AyyQGkX2Y13f9BtwFnzByrrsZwrWTaJtPJh7BRV/unsigned.json'))
        self.assertEqual(expected, actual)
