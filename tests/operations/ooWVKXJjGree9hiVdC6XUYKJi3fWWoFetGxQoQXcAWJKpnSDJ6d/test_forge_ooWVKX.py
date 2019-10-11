from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooWVKX(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooWVKX(self):
        expected = get_data(
            path='operations/ooWVKXJjGree9hiVdC6XUYKJi3fWWoFetGxQoQXcAWJKpnSDJ6d/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooWVKXJjGree9hiVdC6XUYKJi3fWWoFetGxQoQXcAWJKpnSDJ6d/unsigned.json'))
        self.assertEqual(expected, actual)
