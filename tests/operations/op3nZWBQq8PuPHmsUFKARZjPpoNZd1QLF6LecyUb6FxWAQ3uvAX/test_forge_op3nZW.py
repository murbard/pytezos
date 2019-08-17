from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop3nZW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op3nZW(self):
        expected = get_data(
            path='operations/op3nZWBQq8PuPHmsUFKARZjPpoNZd1QLF6LecyUb6FxWAQ3uvAX/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op3nZWBQq8PuPHmsUFKARZjPpoNZd1QLF6LecyUb6FxWAQ3uvAX/unsigned.json'))
        self.assertEqual(expected, actual)
