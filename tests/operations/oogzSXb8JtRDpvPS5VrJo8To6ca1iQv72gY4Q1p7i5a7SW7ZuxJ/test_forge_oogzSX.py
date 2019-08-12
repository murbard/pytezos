from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoogzSX(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oogzSX(self):
        expected = get_data(
            path='operations/oogzSXb8JtRDpvPS5VrJo8To6ca1iQv72gY4Q1p7i5a7SW7ZuxJ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oogzSXb8JtRDpvPS5VrJo8To6ca1iQv72gY4Q1p7i5a7SW7ZuxJ/unsigned.json'))
        self.assertEqual(expected, actual)
