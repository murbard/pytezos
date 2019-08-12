from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooF3KB(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooF3KB(self):
        expected = get_data(
            path='operations/ooF3KB5xzAYbPujJDcfkWZGSbMJLR8iiWF9MAXuz2uMggxCaCJa/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooF3KB5xzAYbPujJDcfkWZGSbMJLR8iiWF9MAXuz2uMggxCaCJa/unsigned.json'))
        self.assertEqual(expected, actual)
