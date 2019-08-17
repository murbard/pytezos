from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopK46q(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opK46q(self):
        expected = get_data(
            path='operations/opK46qazFEA8j8TUqaB9HD9B5TxPBDsoU42JnSwjBudB8v5MgoZ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opK46qazFEA8j8TUqaB9HD9B5TxPBDsoU42JnSwjBudB8v5MgoZ/unsigned.json'))
        self.assertEqual(expected, actual)
