from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopS5xd(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opS5xd(self):
        expected = get_data(
            path='operations/opS5xdHMXyLYVhuAfSuihN3FNz6VEw3f9DRdjmUbQwxM9apeXpR/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opS5xdHMXyLYVhuAfSuihN3FNz6VEw3f9DRdjmUbQwxM9apeXpR/unsigned.json'))
        self.assertEqual(expected, actual)
