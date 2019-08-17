from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestood85r(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ood85r(self):
        expected = get_data(
            path='operations/ood85rY6o5QvUjYdbmfqW6cA3uau5rQqrL9r489yhFSccJcGKTr/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ood85rY6o5QvUjYdbmfqW6cA3uau5rQqrL9r489yhFSccJcGKTr/unsigned.json'))
        self.assertEqual(expected, actual)
