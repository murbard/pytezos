from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooaXxp(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooaXxp(self):
        expected = get_data(
            path='operations/ooaXxpA2ZmVQ6z7L473vbVSKCCqZiAmgRdDUZXrExzhkSWJEqK7/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooaXxpA2ZmVQ6z7L473vbVSKCCqZiAmgRdDUZXrExzhkSWJEqK7/unsigned.json'))
        self.assertEqual(expected, actual)
