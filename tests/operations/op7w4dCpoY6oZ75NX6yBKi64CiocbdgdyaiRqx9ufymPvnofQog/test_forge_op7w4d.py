from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop7w4d(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op7w4d(self):
        expected = get_data(
            path='operations/op7w4dCpoY6oZ75NX6yBKi64CiocbdgdyaiRqx9ufymPvnofQog/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op7w4dCpoY6oZ75NX6yBKi64CiocbdgdyaiRqx9ufymPvnofQog/unsigned.json'))
        self.assertEqual(expected, actual)
