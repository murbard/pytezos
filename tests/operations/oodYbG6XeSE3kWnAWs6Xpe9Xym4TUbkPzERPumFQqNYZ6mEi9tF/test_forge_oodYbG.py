from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoodYbG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oodYbG(self):
        expected = get_data(
            path='operations/oodYbG6XeSE3kWnAWs6Xpe9Xym4TUbkPzERPumFQqNYZ6mEi9tF/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oodYbG6XeSE3kWnAWs6Xpe9Xym4TUbkPzERPumFQqNYZ6mEi9tF/unsigned.json'))
        self.assertEqual(expected, actual)
