from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooACpw(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooACpw(self):
        expected = get_data(
            path='operations/ooACpwubtqwp3WNzqvdgtvn9ZzPnxwUvZEFV9Nk9RFndvvDjhwD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooACpwubtqwp3WNzqvdgtvn9ZzPnxwUvZEFV9Nk9RFndvvDjhwD/unsigned.json'))
        self.assertEqual(expected, actual)
