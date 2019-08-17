from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopMgwH(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opMgwH(self):
        expected = get_data(
            path='operations/opMgwHS6m1D1YcKtt6aUXUhQg5F2CJn3WGhg7syKCKeQU5brNq6/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opMgwHS6m1D1YcKtt6aUXUhQg5F2CJn3WGhg7syKCKeQU5brNq6/unsigned.json'))
        self.assertEqual(expected, actual)
