from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooXNAs(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooXNAs(self):
        expected = get_data(
            path='operations/ooXNAsKcKUhonaDvA1wLk5yMCvJPwYMAVuJySMNVjPfWsVNumxc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooXNAsKcKUhonaDvA1wLk5yMCvJPwYMAVuJySMNVjPfWsVNumxc/unsigned.json'))
        self.assertEqual(expected, actual)
