from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooii6N(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooii6N(self):
        expected = get_data(
            path='operations/ooii6NxysLxamKpf4jX3e6MaRVQj2jJE5wSDwtrdq9GsgcA93qS/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooii6NxysLxamKpf4jX3e6MaRVQj2jJE5wSDwtrdq9GsgcA93qS/unsigned.json'))
        self.assertEqual(expected, actual)
