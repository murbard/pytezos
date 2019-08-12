from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooi9Nz(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooi9Nz(self):
        expected = get_data(
            path='operations/ooi9Nz4duRAJzTp9JdcNPpUzx69qS8bL4VTJTy9TBwhcKvH59Qb/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooi9Nz4duRAJzTp9JdcNPpUzx69qS8bL4VTJTy9TBwhcKvH59Qb/unsigned.json'))
        self.assertEqual(expected, actual)
