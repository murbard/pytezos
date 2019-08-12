from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopR49n(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opR49n(self):
        expected = get_data(
            path='operations/opR49nCZvdsKA5bkg3nfmcAVbktbcNJEW1wRcRj3XhroV1WuQdr/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opR49nCZvdsKA5bkg3nfmcAVbktbcNJEW1wRcRj3XhroV1WuQdr/unsigned.json'))
        self.assertEqual(expected, actual)
