from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooMFG9(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooMFG9(self):
        expected = get_data(
            path='operations/ooMFG9uTMQ3ECT4cr1Cm3WCex9qKTQkuBbfHxhK2VM2BdhfPuhc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooMFG9uTMQ3ECT4cr1Cm3WCex9qKTQkuBbfHxhK2VM2BdhfPuhc/unsigned.json'))
        self.assertEqual(expected, actual)
