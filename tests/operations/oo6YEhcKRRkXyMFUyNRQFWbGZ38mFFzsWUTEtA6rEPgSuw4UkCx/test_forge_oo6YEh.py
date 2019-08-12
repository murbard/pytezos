from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo6YEh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo6YEh(self):
        expected = get_data(
            path='operations/oo6YEhcKRRkXyMFUyNRQFWbGZ38mFFzsWUTEtA6rEPgSuw4UkCx/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo6YEhcKRRkXyMFUyNRQFWbGZ38mFFzsWUTEtA6rEPgSuw4UkCx/unsigned.json'))
        self.assertEqual(expected, actual)
