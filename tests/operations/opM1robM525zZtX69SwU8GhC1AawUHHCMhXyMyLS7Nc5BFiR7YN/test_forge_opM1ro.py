from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopM1ro(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opM1ro(self):
        expected = get_data(
            path='operations/opM1robM525zZtX69SwU8GhC1AawUHHCMhXyMyLS7Nc5BFiR7YN/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opM1robM525zZtX69SwU8GhC1AawUHHCMhXyMyLS7Nc5BFiR7YN/unsigned.json'))
        self.assertEqual(expected, actual)
