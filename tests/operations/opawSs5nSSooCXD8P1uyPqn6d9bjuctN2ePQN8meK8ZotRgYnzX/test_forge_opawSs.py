from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopawSs(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opawSs(self):
        expected = get_data(
            path='operations/opawSs5nSSooCXD8P1uyPqn6d9bjuctN2ePQN8meK8ZotRgYnzX/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opawSs5nSSooCXD8P1uyPqn6d9bjuctN2ePQN8meK8ZotRgYnzX/unsigned.json'))
        self.assertEqual(expected, actual)
