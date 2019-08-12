from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonhKhK(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onhKhK(self):
        expected = get_data(
            path='operations/onhKhKLpV8FRrrBdUJ5pxUv5dvU5NsBgXhrLcVPiTwT7Kk8jTbU/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onhKhKLpV8FRrrBdUJ5pxUv5dvU5NsBgXhrLcVPiTwT7Kk8jTbU/unsigned.json'))
        self.assertEqual(expected, actual)
