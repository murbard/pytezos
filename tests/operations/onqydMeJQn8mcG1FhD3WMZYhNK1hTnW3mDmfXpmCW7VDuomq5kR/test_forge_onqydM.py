from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonqydM(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onqydM(self):
        expected = get_data(
            path='operations/onqydMeJQn8mcG1FhD3WMZYhNK1hTnW3mDmfXpmCW7VDuomq5kR/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onqydMeJQn8mcG1FhD3WMZYhNK1hTnW3mDmfXpmCW7VDuomq5kR/unsigned.json'))
        self.assertEqual(expected, actual)
