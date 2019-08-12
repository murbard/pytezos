from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopCR4J(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opCR4J(self):
        expected = get_data(
            path='operations/opCR4J7ZfSYTihQNLa8PNErTtbai8QHWchSttZnbv5zhj27kKb4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opCR4J7ZfSYTihQNLa8PNErTtbai8QHWchSttZnbv5zhj27kKb4/unsigned.json'))
        self.assertEqual(expected, actual)
