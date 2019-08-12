from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoodcXr(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oodcXr(self):
        expected = get_data(
            path='operations/oodcXrZZ5hjuytTfx6m2pYUkwzKBYbA8bYV8uVdgcDgB7ifmmDv/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oodcXrZZ5hjuytTfx6m2pYUkwzKBYbA8bYV8uVdgcDgB7ifmmDv/unsigned.json'))
        self.assertEqual(expected, actual)
