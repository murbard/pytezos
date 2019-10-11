from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopNKxd(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opNKxd(self):
        expected = get_data(
            path='operations/opNKxdaXJMeVLHgz3DWrMyVR1Ni9k8seQhvCDWfeL33Ff5fRXDh/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opNKxdaXJMeVLHgz3DWrMyVR1Ni9k8seQhvCDWfeL33Ff5fRXDh/unsigned.json'))
        self.assertEqual(expected, actual)
