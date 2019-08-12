from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoozsvS(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oozsvS(self):
        expected = get_data(
            path='operations/oozsvSc9nF49WiDrNPytHD2tNQRyZ4uR4KT56PVikisfzLFveU5/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oozsvSc9nF49WiDrNPytHD2tNQRyZ4uR4KT56PVikisfzLFveU5/unsigned.json'))
        self.assertEqual(expected, actual)
