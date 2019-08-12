from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopQ4AN(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opQ4AN(self):
        expected = get_data(
            path='operations/opQ4ANcmQaeQqqLj9hceTD7T6KoLg3QxHN1AmkGRHEPQxLVpWFB/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opQ4ANcmQaeQqqLj9hceTD7T6KoLg3QxHN1AmkGRHEPQxLVpWFB/unsigned.json'))
        self.assertEqual(expected, actual)
