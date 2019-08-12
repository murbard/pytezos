from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonxjHQ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onxjHQ(self):
        expected = get_data(
            path='operations/onxjHQip3iKV162YBRUdPiueruyGPKe8cHrobkU5ajJzNcZVZGn/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onxjHQip3iKV162YBRUdPiueruyGPKe8cHrobkU5ajJzNcZVZGn/unsigned.json'))
        self.assertEqual(expected, actual)
