from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooRnzi(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooRnzi(self):
        expected = get_data(
            path='operations/ooRnziVtQoAkiRYhU3gEgsfy6auTxxqT8Y7myMqrVWtcf4isKAA/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooRnziVtQoAkiRYhU3gEgsfy6auTxxqT8Y7myMqrVWtcf4isKAA/unsigned.json'))
        self.assertEqual(expected, actual)
