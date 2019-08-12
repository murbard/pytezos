from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo7Sch(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo7Sch(self):
        expected = get_data(
            path='operations/oo7Sch4wNssPM95i1K1SXbUHCrSLzknePZ1GHoEtyq2v5DistCE/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo7Sch4wNssPM95i1K1SXbUHCrSLzknePZ1GHoEtyq2v5DistCE/unsigned.json'))
        self.assertEqual(expected, actual)
