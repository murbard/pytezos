from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooDRC4(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooDRC4(self):
        expected = get_data(
            path='operations/ooDRC4AkfJJG3X5DmmQUH1AnqrAGefFx3DrPxvtipeUV1hQNE3N/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooDRC4AkfJJG3X5DmmQUH1AnqrAGefFx3DrPxvtipeUV1hQNE3N/unsigned.json'))
        self.assertEqual(expected, actual)
