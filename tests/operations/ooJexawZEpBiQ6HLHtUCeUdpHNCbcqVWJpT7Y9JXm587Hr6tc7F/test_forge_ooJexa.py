from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooJexa(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooJexa(self):
        expected = get_data(
            path='operations/ooJexawZEpBiQ6HLHtUCeUdpHNCbcqVWJpT7Y9JXm587Hr6tc7F/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooJexawZEpBiQ6HLHtUCeUdpHNCbcqVWJpT7Y9JXm587Hr6tc7F/unsigned.json'))
        self.assertEqual(expected, actual)
