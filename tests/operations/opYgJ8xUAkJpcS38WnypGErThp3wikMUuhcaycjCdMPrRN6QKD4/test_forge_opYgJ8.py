from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopYgJ8(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opYgJ8(self):
        expected = get_data(
            path='operations/opYgJ8xUAkJpcS38WnypGErThp3wikMUuhcaycjCdMPrRN6QKD4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opYgJ8xUAkJpcS38WnypGErThp3wikMUuhcaycjCdMPrRN6QKD4/unsigned.json'))
        self.assertEqual(expected, actual)
