from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooqCBy(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooqCBy(self):
        expected = get_data(
            path='operations/ooqCByHWoh19rfTJyjxbn8vuR366AvZ2UqK1kDQAHXMmMtEGoXK/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooqCByHWoh19rfTJyjxbn8vuR366AvZ2UqK1kDQAHXMmMtEGoXK/unsigned.json'))
        self.assertEqual(expected, actual)
