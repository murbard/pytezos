from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonwsfi(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onwsfi(self):
        expected = get_data(
            path='operations/onwsfiCLX1pG4BGxfXqWnbhm8RNJ3yFUWQGuEavjfb59v8CcN6w/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onwsfiCLX1pG4BGxfXqWnbhm8RNJ3yFUWQGuEavjfb59v8CcN6w/unsigned.json'))
        self.assertEqual(expected, actual)
