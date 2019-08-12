from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonhuvx(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onhuvx(self):
        expected = get_data(
            path='operations/onhuvxQKkjTRnffJjnFuyFr8jpU5akFURk4PL5tBAZkpqqZMiru/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onhuvxQKkjTRnffJjnFuyFr8jpU5akFURk4PL5tBAZkpqqZMiru/unsigned.json'))
        self.assertEqual(expected, actual)
