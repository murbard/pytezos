from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonhwzh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onhwzh(self):
        expected = get_data(
            path='operations/onhwzhKtwSTwTkbLUna9pRDQ8dXq6bwPSpoZeRkJHFNmAuELtWR/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onhwzhKtwSTwTkbLUna9pRDQ8dXq6bwPSpoZeRkJHFNmAuELtWR/unsigned.json'))
        self.assertEqual(expected, actual)
