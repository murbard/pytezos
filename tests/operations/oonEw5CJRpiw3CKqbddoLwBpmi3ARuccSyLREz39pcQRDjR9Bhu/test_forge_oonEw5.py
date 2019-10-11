from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoonEw5(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oonEw5(self):
        expected = get_data(
            path='operations/oonEw5CJRpiw3CKqbddoLwBpmi3ARuccSyLREz39pcQRDjR9Bhu/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oonEw5CJRpiw3CKqbddoLwBpmi3ARuccSyLREz39pcQRDjR9Bhu/unsigned.json'))
        self.assertEqual(expected, actual)
