from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopLToJ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opLToJ(self):
        expected = get_data(
            path='operations/opLToJmJM6dNrrkPL2sk8kt3jBmoFsEPb6UeGvFmtL7uppxbnQU/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opLToJmJM6dNrrkPL2sk8kt3jBmoFsEPb6UeGvFmtL7uppxbnQU/unsigned.json'))
        self.assertEqual(expected, actual)
