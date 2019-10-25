from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopWjuD(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opWjuD(self):
        expected = get_data(
            path='operations/opWjuDnTDwpYCLEX8Vtm3EgJbvtZLtBVBhDPgDzxwj5BRWTiQFa/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opWjuDnTDwpYCLEX8Vtm3EgJbvtZLtBVBhDPgDzxwj5BRWTiQFa/unsigned.json'))
        self.assertEqual(expected, actual)
