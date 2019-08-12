from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonqCYD(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onqCYD(self):
        expected = get_data(
            path='operations/onqCYDZRnmKkGLo6iUTxY1JYioSZDKt1MRKTM6hkNeA7Xk4JMVJ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onqCYDZRnmKkGLo6iUTxY1JYioSZDKt1MRKTM6hkNeA7Xk4JMVJ/unsigned.json'))
        self.assertEqual(expected, actual)
