from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo4gqK(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo4gqK(self):
        expected = get_data(
            path='operations/oo4gqKSMre4VyWVh5zRScQpBPevwmYbFxNLaSFYzNyUoaz1hL9M/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo4gqKSMre4VyWVh5zRScQpBPevwmYbFxNLaSFYzNyUoaz1hL9M/unsigned.json'))
        self.assertEqual(expected, actual)
