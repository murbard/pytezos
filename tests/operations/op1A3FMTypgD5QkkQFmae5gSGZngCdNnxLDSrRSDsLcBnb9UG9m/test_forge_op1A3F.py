from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop1A3F(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op1A3F(self):
        expected = get_data(
            path='operations/op1A3FMTypgD5QkkQFmae5gSGZngCdNnxLDSrRSDsLcBnb9UG9m/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op1A3FMTypgD5QkkQFmae5gSGZngCdNnxLDSrRSDsLcBnb9UG9m/unsigned.json'))
        self.assertEqual(expected, actual)
