from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop6rQu(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op6rQu(self):
        expected = get_data(
            path='operations/op6rQuXYactN9gCT8mXapcJ64z1r2t7qqBo2PqBnp2rjnKbw4Zz/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op6rQuXYactN9gCT8mXapcJ64z1r2t7qqBo2PqBnp2rjnKbw4Zz/unsigned.json'))
        self.assertEqual(expected, actual)
