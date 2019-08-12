from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopZyKL(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opZyKL(self):
        expected = get_data(
            path='operations/opZyKLaMs7omxLchsMfDhACUByB2QnHCxMaNi2SH2btc8Vwtp8q/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opZyKLaMs7omxLchsMfDhACUByB2QnHCxMaNi2SH2btc8Vwtp8q/unsigned.json'))
        self.assertEqual(expected, actual)
