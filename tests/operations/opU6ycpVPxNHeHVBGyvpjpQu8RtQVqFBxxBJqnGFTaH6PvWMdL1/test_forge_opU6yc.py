from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopU6yc(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opU6yc(self):
        expected = get_data(
            path='operations/opU6ycpVPxNHeHVBGyvpjpQu8RtQVqFBxxBJqnGFTaH6PvWMdL1/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opU6ycpVPxNHeHVBGyvpjpQu8RtQVqFBxxBJqnGFTaH6PvWMdL1/unsigned.json'))
        self.assertEqual(expected, actual)
