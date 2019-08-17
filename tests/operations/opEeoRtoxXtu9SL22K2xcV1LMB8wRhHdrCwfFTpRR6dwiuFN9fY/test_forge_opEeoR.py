from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopEeoR(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opEeoR(self):
        expected = get_data(
            path='operations/opEeoRtoxXtu9SL22K2xcV1LMB8wRhHdrCwfFTpRR6dwiuFN9fY/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opEeoRtoxXtu9SL22K2xcV1LMB8wRhHdrCwfFTpRR6dwiuFN9fY/unsigned.json'))
        self.assertEqual(expected, actual)
