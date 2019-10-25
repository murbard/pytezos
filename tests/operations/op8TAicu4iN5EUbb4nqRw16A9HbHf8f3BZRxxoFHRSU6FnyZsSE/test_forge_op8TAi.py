from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop8TAi(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op8TAi(self):
        expected = get_data(
            path='operations/op8TAicu4iN5EUbb4nqRw16A9HbHf8f3BZRxxoFHRSU6FnyZsSE/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op8TAicu4iN5EUbb4nqRw16A9HbHf8f3BZRxxoFHRSU6FnyZsSE/unsigned.json'))
        self.assertEqual(expected, actual)
