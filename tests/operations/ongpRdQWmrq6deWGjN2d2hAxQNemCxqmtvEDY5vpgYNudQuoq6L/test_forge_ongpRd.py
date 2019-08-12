from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestongpRd(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ongpRd(self):
        expected = get_data(
            path='operations/ongpRdQWmrq6deWGjN2d2hAxQNemCxqmtvEDY5vpgYNudQuoq6L/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ongpRdQWmrq6deWGjN2d2hAxQNemCxqmtvEDY5vpgYNudQuoq6L/unsigned.json'))
        self.assertEqual(expected, actual)
