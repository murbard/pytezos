from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooa2MF(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooa2MF(self):
        expected = get_data(
            path='operations/ooa2MFB9vQdwyYVErR4xGmrVm4zZTwxoiwo7fAryetSS2YjVJq4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooa2MFB9vQdwyYVErR4xGmrVm4zZTwxoiwo7fAryetSS2YjVJq4/unsigned.json'))
        self.assertEqual(expected, actual)
