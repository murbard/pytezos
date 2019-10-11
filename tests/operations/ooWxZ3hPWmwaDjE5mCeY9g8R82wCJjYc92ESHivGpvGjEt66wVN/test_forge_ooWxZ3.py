from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooWxZ3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooWxZ3(self):
        expected = get_data(
            path='operations/ooWxZ3hPWmwaDjE5mCeY9g8R82wCJjYc92ESHivGpvGjEt66wVN/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooWxZ3hPWmwaDjE5mCeY9g8R82wCJjYc92ESHivGpvGjEt66wVN/unsigned.json'))
        self.assertEqual(expected, actual)
