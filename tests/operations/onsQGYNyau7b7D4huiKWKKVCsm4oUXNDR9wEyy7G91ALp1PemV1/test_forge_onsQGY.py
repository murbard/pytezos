from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonsQGY(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onsQGY(self):
        expected = get_data(
            path='operations/onsQGYNyau7b7D4huiKWKKVCsm4oUXNDR9wEyy7G91ALp1PemV1/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onsQGYNyau7b7D4huiKWKKVCsm4oUXNDR9wEyy7G91ALp1PemV1/unsigned.json'))
        self.assertEqual(expected, actual)
