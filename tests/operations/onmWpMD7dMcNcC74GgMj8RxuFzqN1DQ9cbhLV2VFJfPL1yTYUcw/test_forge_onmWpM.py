from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonmWpM(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onmWpM(self):
        expected = get_data(
            path='operations/onmWpMD7dMcNcC74GgMj8RxuFzqN1DQ9cbhLV2VFJfPL1yTYUcw/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onmWpMD7dMcNcC74GgMj8RxuFzqN1DQ9cbhLV2VFJfPL1yTYUcw/unsigned.json'))
        self.assertEqual(expected, actual)
