from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooz1K2(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooz1K2(self):
        expected = get_data(
            path='operations/ooz1K2QpPkh25YnBVHkcRDoAM29vnXrKsQqpDHjxZxE2yR1akUM/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooz1K2QpPkh25YnBVHkcRDoAM29vnXrKsQqpDHjxZxE2yR1akUM/unsigned.json'))
        self.assertEqual(expected, actual)
