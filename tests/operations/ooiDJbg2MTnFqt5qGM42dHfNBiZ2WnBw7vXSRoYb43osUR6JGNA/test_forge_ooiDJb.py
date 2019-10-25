from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooiDJb(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooiDJb(self):
        expected = get_data(
            path='operations/ooiDJbg2MTnFqt5qGM42dHfNBiZ2WnBw7vXSRoYb43osUR6JGNA/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooiDJbg2MTnFqt5qGM42dHfNBiZ2WnBw7vXSRoYb43osUR6JGNA/unsigned.json'))
        self.assertEqual(expected, actual)
