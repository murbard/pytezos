from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooT7DV(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooT7DV(self):
        expected = get_data(
            path='operations/ooT7DVP4r5qYqVHEiJdYRDaeTSk4B4UwQe1B2BUq47FwPJ76R17/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooT7DVP4r5qYqVHEiJdYRDaeTSk4B4UwQe1B2BUq47FwPJ76R17/unsigned.json'))
        self.assertEqual(expected, actual)
