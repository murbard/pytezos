from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonvutm(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onvutm(self):
        expected = get_data(
            path='operations/onvutm26XPQ9yEwNHXYWBB1Rpgp5Nc76AswZTKaHrTUwfRRwVMD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onvutm26XPQ9yEwNHXYWBB1Rpgp5Nc76AswZTKaHrTUwfRRwVMD/unsigned.json'))
        self.assertEqual(expected, actual)
