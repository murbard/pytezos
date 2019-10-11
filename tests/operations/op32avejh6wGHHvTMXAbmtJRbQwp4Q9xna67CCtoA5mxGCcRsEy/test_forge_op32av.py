from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop32av(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op32av(self):
        expected = get_data(
            path='operations/op32avejh6wGHHvTMXAbmtJRbQwp4Q9xna67CCtoA5mxGCcRsEy/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op32avejh6wGHHvTMXAbmtJRbQwp4Q9xna67CCtoA5mxGCcRsEy/unsigned.json'))
        self.assertEqual(expected, actual)
