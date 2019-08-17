from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo781h(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo781h(self):
        expected = get_data(
            path='operations/oo781hV9VbNomfWSb7gtNKm3eUUj7c8ayns1SvcXXwhXgkk28mu/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo781hV9VbNomfWSb7gtNKm3eUUj7c8ayns1SvcXXwhXgkk28mu/unsigned.json'))
        self.assertEqual(expected, actual)
