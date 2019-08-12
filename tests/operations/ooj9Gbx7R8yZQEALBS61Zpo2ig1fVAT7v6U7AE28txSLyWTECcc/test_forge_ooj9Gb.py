from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooj9Gb(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooj9Gb(self):
        expected = get_data(
            path='operations/ooj9Gbx7R8yZQEALBS61Zpo2ig1fVAT7v6U7AE28txSLyWTECcc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooj9Gbx7R8yZQEALBS61Zpo2ig1fVAT7v6U7AE28txSLyWTECcc/unsigned.json'))
        self.assertEqual(expected, actual)
