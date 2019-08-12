from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooEqoS(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooEqoS(self):
        expected = get_data(
            path='operations/ooEqoSMLiBJVjJBS1sVhjKp4KqNa5bv1zPVtQaDBqKdYdtirTz9/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooEqoSMLiBJVjJBS1sVhjKp4KqNa5bv1zPVtQaDBqKdYdtirTz9/unsigned.json'))
        self.assertEqual(expected, actual)
