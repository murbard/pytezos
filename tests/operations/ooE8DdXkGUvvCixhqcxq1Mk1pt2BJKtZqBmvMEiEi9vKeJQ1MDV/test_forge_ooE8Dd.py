from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooE8Dd(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooE8Dd(self):
        expected = get_data(
            path='operations/ooE8DdXkGUvvCixhqcxq1Mk1pt2BJKtZqBmvMEiEi9vKeJQ1MDV/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooE8DdXkGUvvCixhqcxq1Mk1pt2BJKtZqBmvMEiEi9vKeJQ1MDV/unsigned.json'))
        self.assertEqual(expected, actual)
