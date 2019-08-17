from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonxYg4(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onxYg4(self):
        expected = get_data(
            path='operations/onxYg4DXZrg53umkr6APfUkJGJTodMvLrg5CvXumA72fzvsy43j/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onxYg4DXZrg53umkr6APfUkJGJTodMvLrg5CvXumA72fzvsy43j/unsigned.json'))
        self.assertEqual(expected, actual)
