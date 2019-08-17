from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopQg8n(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opQg8n(self):
        expected = get_data(
            path='operations/opQg8nwr7MjDuYqUG349MV4txmnTytKpyss3HuewdqQu8ZYg4zS/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opQg8nwr7MjDuYqUG349MV4txmnTytKpyss3HuewdqQu8ZYg4zS/unsigned.json'))
        self.assertEqual(expected, actual)
