from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo7Xvv(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo7Xvv(self):
        expected = get_data(
            path='operations/oo7XvvBvmNWKW6BTrNkm7Px3suKD9FPtNjAb9tzCG2s7xKzv3CZ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo7XvvBvmNWKW6BTrNkm7Px3suKD9FPtNjAb9tzCG2s7xKzv3CZ/unsigned.json'))
        self.assertEqual(expected, actual)
