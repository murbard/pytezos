from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopKsM9(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opKsM9(self):
        expected = get_data(
            path='operations/opKsM9CB5QSfRe5T6dJexkXXhbJLmqho552sqNgd4uZDQgYYz3K/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opKsM9CB5QSfRe5T6dJexkXXhbJLmqho552sqNgd4uZDQgYYz3K/unsigned.json'))
        self.assertEqual(expected, actual)
