from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopB5Zk(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opB5Zk(self):
        expected = get_data(
            path='operations/opB5ZkGTwV9uttotEApj9dBkQYBg61cPESRUDS2DsUzVRRPkJtv/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opB5ZkGTwV9uttotEApj9dBkQYBg61cPESRUDS2DsUzVRRPkJtv/unsigned.json'))
        self.assertEqual(expected, actual)
