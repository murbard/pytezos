from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoohdw7(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oohdw7(self):
        expected = get_data(
            path='operations/oohdw7BEgesjWcJUBnkPcK7MCtkDth5aW1Cn4zqtHjGxpCNryFQ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oohdw7BEgesjWcJUBnkPcK7MCtkDth5aW1Cn4zqtHjGxpCNryFQ/unsigned.json'))
        self.assertEqual(expected, actual)
