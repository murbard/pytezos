from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopJK2r(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opJK2r(self):
        expected = get_data(
            path='operations/opJK2rMC6CXNbpZmYhdKXLiabKbcQ92oK7Dr6THAk6TLxqVE22B/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opJK2rMC6CXNbpZmYhdKXLiabKbcQ92oK7Dr6THAk6TLxqVE22B/unsigned.json'))
        self.assertEqual(expected, actual)
