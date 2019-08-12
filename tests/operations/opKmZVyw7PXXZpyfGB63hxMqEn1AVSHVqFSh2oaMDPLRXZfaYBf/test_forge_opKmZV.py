from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopKmZV(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opKmZV(self):
        expected = get_data(
            path='operations/opKmZVyw7PXXZpyfGB63hxMqEn1AVSHVqFSh2oaMDPLRXZfaYBf/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opKmZVyw7PXXZpyfGB63hxMqEn1AVSHVqFSh2oaMDPLRXZfaYBf/unsigned.json'))
        self.assertEqual(expected, actual)
