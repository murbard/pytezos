from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopaTwM(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opaTwM(self):
        expected = get_data(
            path='operations/opaTwM259eqyyNZtLUESJ3EadfKNzRDPMoDA3jC59hNBwBogDaF/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opaTwM259eqyyNZtLUESJ3EadfKNzRDPMoDA3jC59hNBwBogDaF/unsigned.json'))
        self.assertEqual(expected, actual)
