from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopMpPh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opMpPh(self):
        expected = get_data(
            path='operations/opMpPhJzAL1zunLsad8Q36dFXpWwGYSkHhrpgeSuwfSHGn1imVs/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opMpPhJzAL1zunLsad8Q36dFXpWwGYSkHhrpgeSuwfSHGn1imVs/unsigned.json'))
        self.assertEqual(expected, actual)
