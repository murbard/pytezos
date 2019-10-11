from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopHREP(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opHREP(self):
        expected = get_data(
            path='operations/opHREPDBwXeAgA1fQKQZ8e8t8L93LZfX38cy5xMsHeCdf8x59x6/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opHREPDBwXeAgA1fQKQZ8e8t8L93LZfX38cy5xMsHeCdf8x59x6/unsigned.json'))
        self.assertEqual(expected, actual)
