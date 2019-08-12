from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonzgMw(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onzgMw(self):
        expected = get_data(
            path='operations/onzgMwHxYevvzhp9y45CuPUcnxh2aPtN9DdM5VZ4yDkQK6zazj9/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onzgMwHxYevvzhp9y45CuPUcnxh2aPtN9DdM5VZ4yDkQK6zazj9/unsigned.json'))
        self.assertEqual(expected, actual)
