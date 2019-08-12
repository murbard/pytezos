from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooU7GS(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooU7GS(self):
        expected = get_data(
            path='operations/ooU7GSEcqyMXR9FJAsiFToEysY4smXkar5pdVTu5LRfYSV5Lw8s/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooU7GSEcqyMXR9FJAsiFToEysY4smXkar5pdVTu5LRfYSV5Lw8s/unsigned.json'))
        self.assertEqual(expected, actual)
