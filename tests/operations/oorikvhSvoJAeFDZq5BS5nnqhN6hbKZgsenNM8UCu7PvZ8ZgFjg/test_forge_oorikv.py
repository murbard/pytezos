from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoorikv(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oorikv(self):
        expected = get_data(
            path='operations/oorikvhSvoJAeFDZq5BS5nnqhN6hbKZgsenNM8UCu7PvZ8ZgFjg/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oorikvhSvoJAeFDZq5BS5nnqhN6hbKZgsenNM8UCu7PvZ8ZgFjg/unsigned.json'))
        self.assertEqual(expected, actual)
