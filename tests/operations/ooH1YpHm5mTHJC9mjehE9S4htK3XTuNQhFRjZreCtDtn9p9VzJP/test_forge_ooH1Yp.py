from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooH1Yp(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooH1Yp(self):
        expected = get_data(
            path='operations/ooH1YpHm5mTHJC9mjehE9S4htK3XTuNQhFRjZreCtDtn9p9VzJP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooH1YpHm5mTHJC9mjehE9S4htK3XTuNQhFRjZreCtDtn9p9VzJP/unsigned.json'))
        self.assertEqual(expected, actual)
