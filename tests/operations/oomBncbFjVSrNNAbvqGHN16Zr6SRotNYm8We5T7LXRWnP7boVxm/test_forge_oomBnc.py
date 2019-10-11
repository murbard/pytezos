from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoomBnc(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oomBnc(self):
        expected = get_data(
            path='operations/oomBncbFjVSrNNAbvqGHN16Zr6SRotNYm8We5T7LXRWnP7boVxm/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oomBncbFjVSrNNAbvqGHN16Zr6SRotNYm8We5T7LXRWnP7boVxm/unsigned.json'))
        self.assertEqual(expected, actual)
