from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopaMPy(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opaMPy(self):
        expected = get_data(
            path='operations/opaMPyHq5VATkiBLsuzBDgtS9dvdzQh77NawbVZMqqYi9EWiEwZ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opaMPyHq5VATkiBLsuzBDgtS9dvdzQh77NawbVZMqqYi9EWiEwZ/unsigned.json'))
        self.assertEqual(expected, actual)
