from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopFf4e(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opFf4e(self):
        expected = get_data(
            path='operations/opFf4eZwDStrDUnXtu1CPMfmPq1AyUHyKN1iLjZTH2WX8JomkBz/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opFf4eZwDStrDUnXtu1CPMfmPq1AyUHyKN1iLjZTH2WX8JomkBz/unsigned.json'))
        self.assertEqual(expected, actual)
