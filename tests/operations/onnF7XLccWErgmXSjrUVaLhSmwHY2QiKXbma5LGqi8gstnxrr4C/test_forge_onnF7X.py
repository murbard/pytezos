from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonnF7X(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onnF7X(self):
        expected = get_data(
            path='operations/onnF7XLccWErgmXSjrUVaLhSmwHY2QiKXbma5LGqi8gstnxrr4C/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onnF7XLccWErgmXSjrUVaLhSmwHY2QiKXbma5LGqi8gstnxrr4C/unsigned.json'))
        self.assertEqual(expected, actual)
