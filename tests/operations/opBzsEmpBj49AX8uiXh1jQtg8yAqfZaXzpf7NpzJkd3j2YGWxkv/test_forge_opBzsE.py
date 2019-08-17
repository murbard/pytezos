from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopBzsE(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opBzsE(self):
        expected = get_data(
            path='operations/opBzsEmpBj49AX8uiXh1jQtg8yAqfZaXzpf7NpzJkd3j2YGWxkv/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opBzsEmpBj49AX8uiXh1jQtg8yAqfZaXzpf7NpzJkd3j2YGWxkv/unsigned.json'))
        self.assertEqual(expected, actual)
