from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonxWho(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onxWho(self):
        expected = get_data(
            path='operations/onxWhoHCwb9WKHDtxauco5rfik94d2FSm4Rhy3Z5gd2WcqHpjAJ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onxWhoHCwb9WKHDtxauco5rfik94d2FSm4Rhy3Z5gd2WcqHpjAJ/unsigned.json'))
        self.assertEqual(expected, actual)
