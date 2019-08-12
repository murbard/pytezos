from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoniiMp(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oniiMp(self):
        expected = get_data(
            path='operations/oniiMpmdUZ6yJSwe11L4f4kmo43yRgRV6N5gakmGeYNSYscSQXk/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oniiMpmdUZ6yJSwe11L4f4kmo43yRgRV6N5gakmGeYNSYscSQXk/unsigned.json'))
        self.assertEqual(expected, actual)
