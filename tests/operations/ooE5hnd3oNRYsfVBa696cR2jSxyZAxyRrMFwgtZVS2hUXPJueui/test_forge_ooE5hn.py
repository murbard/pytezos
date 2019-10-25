from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooE5hn(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooE5hn(self):
        expected = get_data(
            path='operations/ooE5hnd3oNRYsfVBa696cR2jSxyZAxyRrMFwgtZVS2hUXPJueui/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooE5hnd3oNRYsfVBa696cR2jSxyZAxyRrMFwgtZVS2hUXPJueui/unsigned.json'))
        self.assertEqual(expected, actual)
