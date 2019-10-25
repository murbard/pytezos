from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonqXR6(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onqXR6(self):
        expected = get_data(
            path='operations/onqXR6C49AUi6iKC3m3i2uopRckrZNsUJ4PGtoXcTXSVMSt1qir/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onqXR6C49AUi6iKC3m3i2uopRckrZNsUJ4PGtoXcTXSVMSt1qir/unsigned.json'))
        self.assertEqual(expected, actual)
