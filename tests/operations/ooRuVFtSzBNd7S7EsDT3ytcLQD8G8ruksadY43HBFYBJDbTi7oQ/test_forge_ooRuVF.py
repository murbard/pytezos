from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooRuVF(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooRuVF(self):
        expected = get_data(
            path='operations/ooRuVFtSzBNd7S7EsDT3ytcLQD8G8ruksadY43HBFYBJDbTi7oQ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooRuVFtSzBNd7S7EsDT3ytcLQD8G8ruksadY43HBFYBJDbTi7oQ/unsigned.json'))
        self.assertEqual(expected, actual)
