from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooVSFA(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooVSFA(self):
        expected = get_data(
            path='operations/ooVSFAUYa4Pz5JfpKbBPGn43EhUun4DfF5GvYeTKwwv4x3Sgk4k/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooVSFAUYa4Pz5JfpKbBPGn43EhUun4DfF5GvYeTKwwv4x3Sgk4k/unsigned.json'))
        self.assertEqual(expected, actual)
