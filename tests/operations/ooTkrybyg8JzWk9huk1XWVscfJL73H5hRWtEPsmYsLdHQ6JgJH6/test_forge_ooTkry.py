from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooTkry(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooTkry(self):
        expected = get_data(
            path='operations/ooTkrybyg8JzWk9huk1XWVscfJL73H5hRWtEPsmYsLdHQ6JgJH6/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooTkrybyg8JzWk9huk1XWVscfJL73H5hRWtEPsmYsLdHQ6JgJH6/unsigned.json'))
        self.assertEqual(expected, actual)
