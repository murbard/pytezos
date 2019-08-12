from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopQFB6(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opQFB6(self):
        expected = get_data(
            path='operations/opQFB6QQJEnwUebxtTohmutmopTTuXDSwzPopen2KczKt5QghFY/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opQFB6QQJEnwUebxtTohmutmopTTuXDSwzPopen2KczKt5QghFY/unsigned.json'))
        self.assertEqual(expected, actual)
