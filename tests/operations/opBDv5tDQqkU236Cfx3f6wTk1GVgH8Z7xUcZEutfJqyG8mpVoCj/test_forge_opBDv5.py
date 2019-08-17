from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopBDv5(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opBDv5(self):
        expected = get_data(
            path='operations/opBDv5tDQqkU236Cfx3f6wTk1GVgH8Z7xUcZEutfJqyG8mpVoCj/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opBDv5tDQqkU236Cfx3f6wTk1GVgH8Z7xUcZEutfJqyG8mpVoCj/unsigned.json'))
        self.assertEqual(expected, actual)
