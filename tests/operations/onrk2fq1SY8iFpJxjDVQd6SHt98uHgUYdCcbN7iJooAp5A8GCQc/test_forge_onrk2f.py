from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonrk2f(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onrk2f(self):
        expected = get_data(
            path='operations/onrk2fq1SY8iFpJxjDVQd6SHt98uHgUYdCcbN7iJooAp5A8GCQc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onrk2fq1SY8iFpJxjDVQd6SHt98uHgUYdCcbN7iJooAp5A8GCQc/unsigned.json'))
        self.assertEqual(expected, actual)
