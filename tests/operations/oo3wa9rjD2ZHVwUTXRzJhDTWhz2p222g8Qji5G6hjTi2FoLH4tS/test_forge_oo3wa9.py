from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo3wa9(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo3wa9(self):
        expected = get_data(
            path='operations/oo3wa9rjD2ZHVwUTXRzJhDTWhz2p222g8Qji5G6hjTi2FoLH4tS/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo3wa9rjD2ZHVwUTXRzJhDTWhz2p222g8Qji5G6hjTi2FoLH4tS/unsigned.json'))
        self.assertEqual(expected, actual)
