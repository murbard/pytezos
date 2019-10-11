from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooB9Wq(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooB9Wq(self):
        expected = get_data(
            path='operations/ooB9WquEeTm7nQK5p45niL4kZsMe3UrbndWEzJDRMGz1FYWZXzg/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooB9WquEeTm7nQK5p45niL4kZsMe3UrbndWEzJDRMGz1FYWZXzg/unsigned.json'))
        self.assertEqual(expected, actual)
