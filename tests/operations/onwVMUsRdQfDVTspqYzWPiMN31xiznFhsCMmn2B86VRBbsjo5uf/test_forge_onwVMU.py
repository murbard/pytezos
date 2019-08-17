from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonwVMU(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onwVMU(self):
        expected = get_data(
            path='operations/onwVMUsRdQfDVTspqYzWPiMN31xiznFhsCMmn2B86VRBbsjo5uf/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onwVMUsRdQfDVTspqYzWPiMN31xiznFhsCMmn2B86VRBbsjo5uf/unsigned.json'))
        self.assertEqual(expected, actual)
