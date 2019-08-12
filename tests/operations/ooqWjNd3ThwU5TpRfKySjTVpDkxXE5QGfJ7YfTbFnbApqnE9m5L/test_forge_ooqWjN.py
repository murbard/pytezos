from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooqWjN(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooqWjN(self):
        expected = get_data(
            path='operations/ooqWjNd3ThwU5TpRfKySjTVpDkxXE5QGfJ7YfTbFnbApqnE9m5L/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooqWjNd3ThwU5TpRfKySjTVpDkxXE5QGfJ7YfTbFnbApqnE9m5L/unsigned.json'))
        self.assertEqual(expected, actual)
