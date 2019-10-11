from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooxJc7(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooxJc7(self):
        expected = get_data(
            path='operations/ooxJc71jthdAob2y9gMLMufSn9WiFPiyoF3tzK3HD1cQaefWWET/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooxJc71jthdAob2y9gMLMufSn9WiFPiyoF3tzK3HD1cQaefWWET/unsigned.json'))
        self.assertEqual(expected, actual)
