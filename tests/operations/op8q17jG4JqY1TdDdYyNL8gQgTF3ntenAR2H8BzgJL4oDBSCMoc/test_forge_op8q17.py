from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop8q17(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op8q17(self):
        expected = get_data(
            path='operations/op8q17jG4JqY1TdDdYyNL8gQgTF3ntenAR2H8BzgJL4oDBSCMoc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op8q17jG4JqY1TdDdYyNL8gQgTF3ntenAR2H8BzgJL4oDBSCMoc/unsigned.json'))
        self.assertEqual(expected, actual)
