from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoouqRm(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oouqRm(self):
        expected = get_data(
            path='operations/oouqRm85PXxm7NeWyr2g5MSYadEDngZD1SKw4uCmBpMhSXuGd1J/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oouqRm85PXxm7NeWyr2g5MSYadEDngZD1SKw4uCmBpMhSXuGd1J/unsigned.json'))
        self.assertEqual(expected, actual)
