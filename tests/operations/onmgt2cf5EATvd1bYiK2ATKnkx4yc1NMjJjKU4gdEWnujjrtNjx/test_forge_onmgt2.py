from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonmgt2(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onmgt2(self):
        expected = get_data(
            path='operations/onmgt2cf5EATvd1bYiK2ATKnkx4yc1NMjJjKU4gdEWnujjrtNjx/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onmgt2cf5EATvd1bYiK2ATKnkx4yc1NMjJjKU4gdEWnujjrtNjx/unsigned.json'))
        self.assertEqual(expected, actual)
