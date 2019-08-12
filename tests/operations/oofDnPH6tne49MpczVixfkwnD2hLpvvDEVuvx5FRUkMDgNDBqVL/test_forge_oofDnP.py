from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoofDnP(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oofDnP(self):
        expected = get_data(
            path='operations/oofDnPH6tne49MpczVixfkwnD2hLpvvDEVuvx5FRUkMDgNDBqVL/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oofDnPH6tne49MpczVixfkwnD2hLpvvDEVuvx5FRUkMDgNDBqVL/unsigned.json'))
        self.assertEqual(expected, actual)
