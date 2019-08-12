from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo9Wad(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo9Wad(self):
        expected = get_data(
            path='operations/oo9WadkREF5q7ehPFojseGGCJD6jaze24XXAK6v1ugWkkqnAHoK/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo9WadkREF5q7ehPFojseGGCJD6jaze24XXAK6v1ugWkkqnAHoK/unsigned.json'))
        self.assertEqual(expected, actual)
