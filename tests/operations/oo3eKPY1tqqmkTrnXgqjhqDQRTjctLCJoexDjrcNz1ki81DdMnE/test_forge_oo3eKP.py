from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo3eKP(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo3eKP(self):
        expected = get_data(
            path='operations/oo3eKPY1tqqmkTrnXgqjhqDQRTjctLCJoexDjrcNz1ki81DdMnE/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo3eKPY1tqqmkTrnXgqjhqDQRTjctLCJoexDjrcNz1ki81DdMnE/unsigned.json'))
        self.assertEqual(expected, actual)
