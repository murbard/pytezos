from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooJps3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooJps3(self):
        expected = get_data(
            path='operations/ooJps3zFn12j6Zs4t2Z1EvqU4X3bbWFG1WvYvo8mM9hRtfbhNS5/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooJps3zFn12j6Zs4t2Z1EvqU4X3bbWFG1WvYvo8mM9hRtfbhNS5/unsigned.json'))
        self.assertEqual(expected, actual)
