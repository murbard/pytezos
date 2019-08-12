from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooep4o(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooep4o(self):
        expected = get_data(
            path='operations/ooep4oFGSQda3NL1TSGGXHcW7885siK4Dme2L33ozT2iouoaXq7/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooep4oFGSQda3NL1TSGGXHcW7885siK4Dme2L33ozT2iouoaXq7/unsigned.json'))
        self.assertEqual(expected, actual)
