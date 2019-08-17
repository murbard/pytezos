from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonsBDR(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onsBDR(self):
        expected = get_data(
            path='operations/onsBDR9U7hDTiEoj14qAXsNF4LETJ25ac1zCJqNmthB5bLMErxt/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onsBDR9U7hDTiEoj14qAXsNF4LETJ25ac1zCJqNmthB5bLMErxt/unsigned.json'))
        self.assertEqual(expected, actual)
