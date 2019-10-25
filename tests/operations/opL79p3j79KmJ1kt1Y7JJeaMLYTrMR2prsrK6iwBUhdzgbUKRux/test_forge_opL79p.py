from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopL79p(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opL79p(self):
        expected = get_data(
            path='operations/opL79p3j79KmJ1kt1Y7JJeaMLYTrMR2prsrK6iwBUhdzgbUKRux/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opL79p3j79KmJ1kt1Y7JJeaMLYTrMR2prsrK6iwBUhdzgbUKRux/unsigned.json'))
        self.assertEqual(expected, actual)
