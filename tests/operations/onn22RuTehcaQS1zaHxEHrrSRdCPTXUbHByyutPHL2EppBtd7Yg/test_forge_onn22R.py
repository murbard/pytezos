from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonn22R(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onn22R(self):
        expected = get_data(
            path='operations/onn22RuTehcaQS1zaHxEHrrSRdCPTXUbHByyutPHL2EppBtd7Yg/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onn22RuTehcaQS1zaHxEHrrSRdCPTXUbHByyutPHL2EppBtd7Yg/unsigned.json'))
        self.assertEqual(expected, actual)
