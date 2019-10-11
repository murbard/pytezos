from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopDEik(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opDEik(self):
        expected = get_data(
            path='operations/opDEik7RsNfZMXoJdoLCqRKV4iXj7iCwrW8se98SaXeEF66Kbug/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opDEik7RsNfZMXoJdoLCqRKV4iXj7iCwrW8se98SaXeEF66Kbug/unsigned.json'))
        self.assertEqual(expected, actual)
