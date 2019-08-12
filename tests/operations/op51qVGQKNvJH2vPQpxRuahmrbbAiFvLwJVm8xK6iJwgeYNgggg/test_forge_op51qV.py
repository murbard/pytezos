from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop51qV(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op51qV(self):
        expected = get_data(
            path='operations/op51qVGQKNvJH2vPQpxRuahmrbbAiFvLwJVm8xK6iJwgeYNgggg/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op51qVGQKNvJH2vPQpxRuahmrbbAiFvLwJVm8xK6iJwgeYNgggg/unsigned.json'))
        self.assertEqual(expected, actual)
