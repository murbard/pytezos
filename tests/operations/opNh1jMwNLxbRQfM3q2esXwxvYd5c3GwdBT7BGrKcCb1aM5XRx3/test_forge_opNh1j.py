from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopNh1j(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opNh1j(self):
        expected = get_data(
            path='operations/opNh1jMwNLxbRQfM3q2esXwxvYd5c3GwdBT7BGrKcCb1aM5XRx3/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opNh1jMwNLxbRQfM3q2esXwxvYd5c3GwdBT7BGrKcCb1aM5XRx3/unsigned.json'))
        self.assertEqual(expected, actual)
