from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo2Nzd(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo2Nzd(self):
        expected = get_data(
            path='operations/oo2NzdmfhMapq9MT13SSFM2Np6LtUPxXyvUuHLe27mv5b7GBD6E/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo2NzdmfhMapq9MT13SSFM2Np6LtUPxXyvUuHLe27mv5b7GBD6E/unsigned.json'))
        self.assertEqual(expected, actual)
