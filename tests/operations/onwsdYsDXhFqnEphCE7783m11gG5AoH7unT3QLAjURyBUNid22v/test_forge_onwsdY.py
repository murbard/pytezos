from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonwsdY(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onwsdY(self):
        expected = get_data(
            path='operations/onwsdYsDXhFqnEphCE7783m11gG5AoH7unT3QLAjURyBUNid22v/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onwsdYsDXhFqnEphCE7783m11gG5AoH7unT3QLAjURyBUNid22v/unsigned.json'))
        self.assertEqual(expected, actual)
