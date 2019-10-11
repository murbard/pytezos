from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo89iW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo89iW(self):
        expected = get_data(
            path='operations/oo89iWnZutyptJBgPnyEWQB3TLRtTntZaBonumi2scwHVMVP2MS/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo89iWnZutyptJBgPnyEWQB3TLRtTntZaBonumi2scwHVMVP2MS/unsigned.json'))
        self.assertEqual(expected, actual)
