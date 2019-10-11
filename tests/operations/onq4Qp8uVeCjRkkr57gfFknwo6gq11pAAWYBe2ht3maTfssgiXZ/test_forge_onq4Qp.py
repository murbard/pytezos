from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonq4Qp(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onq4Qp(self):
        expected = get_data(
            path='operations/onq4Qp8uVeCjRkkr57gfFknwo6gq11pAAWYBe2ht3maTfssgiXZ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onq4Qp8uVeCjRkkr57gfFknwo6gq11pAAWYBe2ht3maTfssgiXZ/unsigned.json'))
        self.assertEqual(expected, actual)
