from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopHbNc(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opHbNc(self):
        expected = get_data(
            path='operations/opHbNcUwyKHh2Woh8at9DpvdCRPxGRrXj71q9Nhkboih2NUric4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opHbNcUwyKHh2Woh8at9DpvdCRPxGRrXj71q9Nhkboih2NUric4/unsigned.json'))
        self.assertEqual(expected, actual)
