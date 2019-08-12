from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopU71o(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opU71o(self):
        expected = get_data(
            path='operations/opU71o7W2mZMviBjiAfdhbfjRCGDyb8y3tbk7ps6PH9rTaaNyfi/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opU71o7W2mZMviBjiAfdhbfjRCGDyb8y3tbk7ps6PH9rTaaNyfi/unsigned.json'))
        self.assertEqual(expected, actual)
