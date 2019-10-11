from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopBzpp(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opBzpp(self):
        expected = get_data(
            path='operations/opBzppTRyCc5yYqRMJrSh7ZKbSXv9Mbg8M13e3jdGmgwNRjNWbu/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opBzppTRyCc5yYqRMJrSh7ZKbSXv9Mbg8M13e3jdGmgwNRjNWbu/unsigned.json'))
        self.assertEqual(expected, actual)
