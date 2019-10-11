from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonpt1e(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onpt1e(self):
        expected = get_data(
            path='operations/onpt1eh3pChmFaG1jLityhRcpbda1Fu2a72ozSzo9jfe8FYZ5HP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onpt1eh3pChmFaG1jLityhRcpbda1Fu2a72ozSzo9jfe8FYZ5HP/unsigned.json'))
        self.assertEqual(expected, actual)
