from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonnz8e(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onnz8e(self):
        expected = get_data(
            path='operations/onnz8ef7xrDa3SQxmVf6z7pX6PGW26XMetWqesM7zavPjymAUnA/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onnz8ef7xrDa3SQxmVf6z7pX6PGW26XMetWqesM7zavPjymAUnA/unsigned.json'))
        self.assertEqual(expected, actual)
