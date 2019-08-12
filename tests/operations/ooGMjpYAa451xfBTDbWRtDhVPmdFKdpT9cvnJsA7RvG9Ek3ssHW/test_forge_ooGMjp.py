from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooGMjp(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooGMjp(self):
        expected = get_data(
            path='operations/ooGMjpYAa451xfBTDbWRtDhVPmdFKdpT9cvnJsA7RvG9Ek3ssHW/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooGMjpYAa451xfBTDbWRtDhVPmdFKdpT9cvnJsA7RvG9Ek3ssHW/unsigned.json'))
        self.assertEqual(expected, actual)
