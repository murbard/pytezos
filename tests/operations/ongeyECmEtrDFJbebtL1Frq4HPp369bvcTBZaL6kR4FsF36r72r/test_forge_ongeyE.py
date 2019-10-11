from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestongeyE(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ongeyE(self):
        expected = get_data(
            path='operations/ongeyECmEtrDFJbebtL1Frq4HPp369bvcTBZaL6kR4FsF36r72r/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ongeyECmEtrDFJbebtL1Frq4HPp369bvcTBZaL6kR4FsF36r72r/unsigned.json'))
        self.assertEqual(expected, actual)
