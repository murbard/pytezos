from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopNTzx(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opNTzx(self):
        expected = get_data(
            path='operations/opNTzxDUVSRjTthsHYbrmK94uCSsywTXBtCFbkaejjcTXGkd5JN/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opNTzxDUVSRjTthsHYbrmK94uCSsywTXBtCFbkaejjcTXGkd5JN/unsigned.json'))
        self.assertEqual(expected, actual)
