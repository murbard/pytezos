from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo12Uo(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo12Uo(self):
        expected = get_data(
            path='operations/oo12Uo1YNcPthMahi6vxs4QiTHDoh6CShdPWcCFe8Zh3sL2DZHT/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo12Uo1YNcPthMahi6vxs4QiTHDoh6CShdPWcCFe8Zh3sL2DZHT/unsigned.json'))
        self.assertEqual(expected, actual)
