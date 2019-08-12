from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopVTnG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opVTnG(self):
        expected = get_data(
            path='operations/opVTnGf1ab3W9kxas81KQ3ifSaRNsvcLrJgrG6h2fiCiA6mo4Tm/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opVTnGf1ab3W9kxas81KQ3ifSaRNsvcLrJgrG6h2fiCiA6mo4Tm/unsigned.json'))
        self.assertEqual(expected, actual)
