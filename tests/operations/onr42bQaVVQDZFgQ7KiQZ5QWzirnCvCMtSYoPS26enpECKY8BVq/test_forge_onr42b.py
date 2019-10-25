from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonr42b(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onr42b(self):
        expected = get_data(
            path='operations/onr42bQaVVQDZFgQ7KiQZ5QWzirnCvCMtSYoPS26enpECKY8BVq/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onr42bQaVVQDZFgQ7KiQZ5QWzirnCvCMtSYoPS26enpECKY8BVq/unsigned.json'))
        self.assertEqual(expected, actual)
