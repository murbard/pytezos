from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooDChY(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooDChY(self):
        expected = get_data(
            path='operations/ooDChYBMBsWDufkjyg2rodHSHQHA75L3bD6hCDDSSU63fxCsFox/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooDChYBMBsWDufkjyg2rodHSHQHA75L3bD6hCDDSSU63fxCsFox/unsigned.json'))
        self.assertEqual(expected, actual)
