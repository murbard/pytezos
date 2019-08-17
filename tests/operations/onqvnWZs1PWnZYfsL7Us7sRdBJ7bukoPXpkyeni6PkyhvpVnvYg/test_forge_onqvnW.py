from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonqvnW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onqvnW(self):
        expected = get_data(
            path='operations/onqvnWZs1PWnZYfsL7Us7sRdBJ7bukoPXpkyeni6PkyhvpVnvYg/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onqvnWZs1PWnZYfsL7Us7sRdBJ7bukoPXpkyeni6PkyhvpVnvYg/unsigned.json'))
        self.assertEqual(expected, actual)
