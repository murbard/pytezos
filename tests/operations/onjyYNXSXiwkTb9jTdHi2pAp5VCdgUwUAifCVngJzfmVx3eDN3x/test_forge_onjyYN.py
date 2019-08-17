from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonjyYN(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onjyYN(self):
        expected = get_data(
            path='operations/onjyYNXSXiwkTb9jTdHi2pAp5VCdgUwUAifCVngJzfmVx3eDN3x/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onjyYNXSXiwkTb9jTdHi2pAp5VCdgUwUAifCVngJzfmVx3eDN3x/unsigned.json'))
        self.assertEqual(expected, actual)
