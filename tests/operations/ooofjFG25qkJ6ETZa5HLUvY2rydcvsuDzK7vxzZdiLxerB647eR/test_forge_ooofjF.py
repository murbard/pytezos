from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooofjF(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooofjF(self):
        expected = get_data(
            path='operations/ooofjFG25qkJ6ETZa5HLUvY2rydcvsuDzK7vxzZdiLxerB647eR/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooofjFG25qkJ6ETZa5HLUvY2rydcvsuDzK7vxzZdiLxerB647eR/unsigned.json'))
        self.assertEqual(expected, actual)
