from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoovX6X(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oovX6X(self):
        expected = get_data(
            path='operations/oovX6X3sMVK6KNK85S8D9NJXJcQibpD534ou3PjW5iYakmCwfzh/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oovX6X3sMVK6KNK85S8D9NJXJcQibpD534ou3PjW5iYakmCwfzh/unsigned.json'))
        self.assertEqual(expected, actual)
