from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonik4H(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onik4H(self):
        expected = get_data(
            path='operations/onik4HScQRGwsNys3n1HNs2ZuESfkui5Sib7JgFqGUkcTbv4rZR/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onik4HScQRGwsNys3n1HNs2ZuESfkui5Sib7JgFqGUkcTbv4rZR/unsigned.json'))
        self.assertEqual(expected, actual)
