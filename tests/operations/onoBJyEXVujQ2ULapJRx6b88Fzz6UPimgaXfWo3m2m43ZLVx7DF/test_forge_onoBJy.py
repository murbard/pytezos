from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonoBJy(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onoBJy(self):
        expected = get_data(
            path='operations/onoBJyEXVujQ2ULapJRx6b88Fzz6UPimgaXfWo3m2m43ZLVx7DF/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onoBJyEXVujQ2ULapJRx6b88Fzz6UPimgaXfWo3m2m43ZLVx7DF/unsigned.json'))
        self.assertEqual(expected, actual)
