from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonhJGJ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onhJGJ(self):
        expected = get_data(
            path='operations/onhJGJQpAbrANYL8vsGEjT4mYfbCZUsJu2wEHJYESo73B1pMoUD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onhJGJQpAbrANYL8vsGEjT4mYfbCZUsJu2wEHJYESo73B1pMoUD/unsigned.json'))
        self.assertEqual(expected, actual)
