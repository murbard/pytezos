from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonnYpw(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onnYpw(self):
        expected = get_data(
            path='operations/onnYpwnSFrroXjDpzobJFYvUGN4puRFEVmvDof6F9aqA8wqtw7X/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onnYpwnSFrroXjDpzobJFYvUGN4puRFEVmvDof6F9aqA8wqtw7X/unsigned.json'))
        self.assertEqual(expected, actual)
