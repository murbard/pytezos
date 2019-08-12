from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestontPVP(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ontPVP(self):
        expected = get_data(
            path='operations/ontPVPi1WHxW7x27aiwmpNNiHu3MMtiCBvv7526nNyebJc7mJkD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ontPVPi1WHxW7x27aiwmpNNiHu3MMtiCBvv7526nNyebJc7mJkD/unsigned.json'))
        self.assertEqual(expected, actual)
