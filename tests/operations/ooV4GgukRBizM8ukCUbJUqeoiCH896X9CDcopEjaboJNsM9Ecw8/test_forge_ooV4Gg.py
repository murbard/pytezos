from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooV4Gg(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooV4Gg(self):
        expected = get_data(
            path='operations/ooV4GgukRBizM8ukCUbJUqeoiCH896X9CDcopEjaboJNsM9Ecw8/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooV4GgukRBizM8ukCUbJUqeoiCH896X9CDcopEjaboJNsM9Ecw8/unsigned.json'))
        self.assertEqual(expected, actual)
