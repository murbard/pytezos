from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooXnD9(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooXnD9(self):
        expected = get_data(
            path='operations/ooXnD9no9pFZdxKjNfA2QYNqbQsMkHKxu5YuNxio4aoUBXTnxZC/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooXnD9no9pFZdxKjNfA2QYNqbQsMkHKxu5YuNxio4aoUBXTnxZC/unsigned.json'))
        self.assertEqual(expected, actual)
