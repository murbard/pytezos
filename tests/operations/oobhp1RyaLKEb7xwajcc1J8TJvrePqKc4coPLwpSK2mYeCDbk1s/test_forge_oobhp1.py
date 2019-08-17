from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoobhp1(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oobhp1(self):
        expected = get_data(
            path='operations/oobhp1RyaLKEb7xwajcc1J8TJvrePqKc4coPLwpSK2mYeCDbk1s/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oobhp1RyaLKEb7xwajcc1J8TJvrePqKc4coPLwpSK2mYeCDbk1s/unsigned.json'))
        self.assertEqual(expected, actual)
