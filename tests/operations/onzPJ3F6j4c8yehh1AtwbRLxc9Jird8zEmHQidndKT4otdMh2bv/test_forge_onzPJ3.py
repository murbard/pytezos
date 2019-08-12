from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonzPJ3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onzPJ3(self):
        expected = get_data(
            path='operations/onzPJ3F6j4c8yehh1AtwbRLxc9Jird8zEmHQidndKT4otdMh2bv/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onzPJ3F6j4c8yehh1AtwbRLxc9Jird8zEmHQidndKT4otdMh2bv/unsigned.json'))
        self.assertEqual(expected, actual)
