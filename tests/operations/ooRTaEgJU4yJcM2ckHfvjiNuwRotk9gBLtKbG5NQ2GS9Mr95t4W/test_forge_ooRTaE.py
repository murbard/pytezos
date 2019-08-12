from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooRTaE(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooRTaE(self):
        expected = get_data(
            path='operations/ooRTaEgJU4yJcM2ckHfvjiNuwRotk9gBLtKbG5NQ2GS9Mr95t4W/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooRTaEgJU4yJcM2ckHfvjiNuwRotk9gBLtKbG5NQ2GS9Mr95t4W/unsigned.json'))
        self.assertEqual(expected, actual)
