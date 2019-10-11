from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooRfaU(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooRfaU(self):
        expected = get_data(
            path='operations/ooRfaUBhrmvteFefGFnS339nMYYe3YYAY7z2Ub3rXhw2pVJxnNY/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooRfaUBhrmvteFefGFnS339nMYYe3YYAY7z2Ub3rXhw2pVJxnNY/unsigned.json'))
        self.assertEqual(expected, actual)
