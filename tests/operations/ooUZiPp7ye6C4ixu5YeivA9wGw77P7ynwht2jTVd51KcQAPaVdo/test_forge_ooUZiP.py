from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooUZiP(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooUZiP(self):
        expected = get_data(
            path='operations/ooUZiPp7ye6C4ixu5YeivA9wGw77P7ynwht2jTVd51KcQAPaVdo/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooUZiPp7ye6C4ixu5YeivA9wGw77P7ynwht2jTVd51KcQAPaVdo/unsigned.json'))
        self.assertEqual(expected, actual)
