from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoov36o(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oov36o(self):
        expected = get_data(
            path='operations/oov36o3JDiceT6zHS5Fi6dQTEFjjYgoUSKCDCkU6XbnBsMZQWm9/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oov36o3JDiceT6zHS5Fi6dQTEFjjYgoUSKCDCkU6XbnBsMZQWm9/unsigned.json'))
        self.assertEqual(expected, actual)
