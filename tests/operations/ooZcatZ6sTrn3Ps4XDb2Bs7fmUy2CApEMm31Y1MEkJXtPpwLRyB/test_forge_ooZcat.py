from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooZcat(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooZcat(self):
        expected = get_data(
            path='operations/ooZcatZ6sTrn3Ps4XDb2Bs7fmUy2CApEMm31Y1MEkJXtPpwLRyB/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooZcatZ6sTrn3Ps4XDb2Bs7fmUy2CApEMm31Y1MEkJXtPpwLRyB/unsigned.json'))
        self.assertEqual(expected, actual)
