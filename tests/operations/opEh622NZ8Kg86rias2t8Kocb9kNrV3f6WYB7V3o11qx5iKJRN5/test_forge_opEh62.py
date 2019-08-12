from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopEh62(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opEh62(self):
        expected = get_data(
            path='operations/opEh622NZ8Kg86rias2t8Kocb9kNrV3f6WYB7V3o11qx5iKJRN5/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opEh622NZ8Kg86rias2t8Kocb9kNrV3f6WYB7V3o11qx5iKJRN5/unsigned.json'))
        self.assertEqual(expected, actual)
