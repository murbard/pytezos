from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonxgAD(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onxgAD(self):
        expected = get_data(
            path='operations/onxgADiAHDkV4xKpeLCWLFBxvY3rMQHSjQ9EP1gLtQ56p9mSSJY/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onxgADiAHDkV4xKpeLCWLFBxvY3rMQHSjQ9EP1gLtQ56p9mSSJY/unsigned.json'))
        self.assertEqual(expected, actual)
