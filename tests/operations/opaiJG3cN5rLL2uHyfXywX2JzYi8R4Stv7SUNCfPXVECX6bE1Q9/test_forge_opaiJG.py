from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopaiJG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opaiJG(self):
        expected = get_data(
            path='operations/opaiJG3cN5rLL2uHyfXywX2JzYi8R4Stv7SUNCfPXVECX6bE1Q9/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opaiJG3cN5rLL2uHyfXywX2JzYi8R4Stv7SUNCfPXVECX6bE1Q9/unsigned.json'))
        self.assertEqual(expected, actual)
