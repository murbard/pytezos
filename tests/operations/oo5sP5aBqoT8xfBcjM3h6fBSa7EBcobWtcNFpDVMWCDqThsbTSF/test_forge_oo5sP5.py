from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo5sP5(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo5sP5(self):
        expected = get_data(
            path='operations/oo5sP5aBqoT8xfBcjM3h6fBSa7EBcobWtcNFpDVMWCDqThsbTSF/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo5sP5aBqoT8xfBcjM3h6fBSa7EBcobWtcNFpDVMWCDqThsbTSF/unsigned.json'))
        self.assertEqual(expected, actual)
