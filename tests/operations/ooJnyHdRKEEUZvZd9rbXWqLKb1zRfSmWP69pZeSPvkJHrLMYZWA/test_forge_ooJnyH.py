from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooJnyH(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooJnyH(self):
        expected = get_data(
            path='operations/ooJnyHdRKEEUZvZd9rbXWqLKb1zRfSmWP69pZeSPvkJHrLMYZWA/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooJnyHdRKEEUZvZd9rbXWqLKb1zRfSmWP69pZeSPvkJHrLMYZWA/unsigned.json'))
        self.assertEqual(expected, actual)
