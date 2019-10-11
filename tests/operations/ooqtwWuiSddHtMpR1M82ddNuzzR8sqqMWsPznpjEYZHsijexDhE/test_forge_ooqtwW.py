from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooqtwW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooqtwW(self):
        expected = get_data(
            path='operations/ooqtwWuiSddHtMpR1M82ddNuzzR8sqqMWsPznpjEYZHsijexDhE/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooqtwWuiSddHtMpR1M82ddNuzzR8sqqMWsPznpjEYZHsijexDhE/unsigned.json'))
        self.assertEqual(expected, actual)
