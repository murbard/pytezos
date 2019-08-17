from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonovaT(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onovaT(self):
        expected = get_data(
            path='operations/onovaTVQYbcN8aJkwsH6rjQap8VrAwZzUoS2uL6Ay6L44Zr7fky/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onovaTVQYbcN8aJkwsH6rjQap8VrAwZzUoS2uL6Ay6L44Zr7fky/unsigned.json'))
        self.assertEqual(expected, actual)
