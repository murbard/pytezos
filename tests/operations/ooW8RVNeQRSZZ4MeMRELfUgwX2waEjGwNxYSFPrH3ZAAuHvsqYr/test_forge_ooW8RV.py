from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooW8RV(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooW8RV(self):
        expected = get_data(
            path='operations/ooW8RVNeQRSZZ4MeMRELfUgwX2waEjGwNxYSFPrH3ZAAuHvsqYr/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooW8RVNeQRSZZ4MeMRELfUgwX2waEjGwNxYSFPrH3ZAAuHvsqYr/unsigned.json'))
        self.assertEqual(expected, actual)
