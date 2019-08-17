from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopCbSH(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opCbSH(self):
        expected = get_data(
            path='operations/opCbSHSxojAzF3RKJRpQG7RwCrkYrJuH8kV4FZUU5maP2B3kzgE/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opCbSHSxojAzF3RKJRpQG7RwCrkYrJuH8kV4FZUU5maP2B3kzgE/unsigned.json'))
        self.assertEqual(expected, actual)
