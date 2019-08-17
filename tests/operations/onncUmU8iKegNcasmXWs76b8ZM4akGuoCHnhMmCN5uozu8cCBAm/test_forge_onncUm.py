from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonncUm(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onncUm(self):
        expected = get_data(
            path='operations/onncUmU8iKegNcasmXWs76b8ZM4akGuoCHnhMmCN5uozu8cCBAm/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onncUmU8iKegNcasmXWs76b8ZM4akGuoCHnhMmCN5uozu8cCBAm/unsigned.json'))
        self.assertEqual(expected, actual)
