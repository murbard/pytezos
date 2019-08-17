from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooPEEz(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooPEEz(self):
        expected = get_data(
            path='operations/ooPEEzCUbKqqTpMZzLjBGpaNqxhTTyX5S2EWNkNy2wqZTzpWGUH/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooPEEzCUbKqqTpMZzLjBGpaNqxhTTyX5S2EWNkNy2wqZTzpWGUH/unsigned.json'))
        self.assertEqual(expected, actual)
