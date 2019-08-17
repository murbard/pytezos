from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonwAHh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onwAHh(self):
        expected = get_data(
            path='operations/onwAHh2Q7PGphYYjfcbjona2thRhLx58B6eQctJHsYLTpuxqSwe/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onwAHh2Q7PGphYYjfcbjona2thRhLx58B6eQctJHsYLTpuxqSwe/unsigned.json'))
        self.assertEqual(expected, actual)
