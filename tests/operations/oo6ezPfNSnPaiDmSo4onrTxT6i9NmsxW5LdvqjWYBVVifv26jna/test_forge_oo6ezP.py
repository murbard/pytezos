from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo6ezP(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo6ezP(self):
        expected = get_data(
            path='operations/oo6ezPfNSnPaiDmSo4onrTxT6i9NmsxW5LdvqjWYBVVifv26jna/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo6ezPfNSnPaiDmSo4onrTxT6i9NmsxW5LdvqjWYBVVifv26jna/unsigned.json'))
        self.assertEqual(expected, actual)
