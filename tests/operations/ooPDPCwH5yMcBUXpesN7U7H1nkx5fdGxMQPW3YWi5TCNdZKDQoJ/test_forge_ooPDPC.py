from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooPDPC(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooPDPC(self):
        expected = get_data(
            path='operations/ooPDPCwH5yMcBUXpesN7U7H1nkx5fdGxMQPW3YWi5TCNdZKDQoJ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooPDPCwH5yMcBUXpesN7U7H1nkx5fdGxMQPW3YWi5TCNdZKDQoJ/unsigned.json'))
        self.assertEqual(expected, actual)
