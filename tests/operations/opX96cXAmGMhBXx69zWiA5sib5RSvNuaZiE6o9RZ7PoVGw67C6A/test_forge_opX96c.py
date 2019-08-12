from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopX96c(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opX96c(self):
        expected = get_data(
            path='operations/opX96cXAmGMhBXx69zWiA5sib5RSvNuaZiE6o9RZ7PoVGw67C6A/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opX96cXAmGMhBXx69zWiA5sib5RSvNuaZiE6o9RZ7PoVGw67C6A/unsigned.json'))
        self.assertEqual(expected, actual)
