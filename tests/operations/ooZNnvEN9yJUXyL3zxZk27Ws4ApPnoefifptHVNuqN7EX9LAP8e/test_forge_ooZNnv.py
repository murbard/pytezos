from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooZNnv(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooZNnv(self):
        expected = get_data(
            path='operations/ooZNnvEN9yJUXyL3zxZk27Ws4ApPnoefifptHVNuqN7EX9LAP8e/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooZNnvEN9yJUXyL3zxZk27Ws4ApPnoefifptHVNuqN7EX9LAP8e/unsigned.json'))
        self.assertEqual(expected, actual)
