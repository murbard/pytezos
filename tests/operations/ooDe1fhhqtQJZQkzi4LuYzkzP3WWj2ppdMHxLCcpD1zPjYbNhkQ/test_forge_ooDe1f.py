from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooDe1f(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooDe1f(self):
        expected = get_data(
            path='operations/ooDe1fhhqtQJZQkzi4LuYzkzP3WWj2ppdMHxLCcpD1zPjYbNhkQ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooDe1fhhqtQJZQkzi4LuYzkzP3WWj2ppdMHxLCcpD1zPjYbNhkQ/unsigned.json'))
        self.assertEqual(expected, actual)
