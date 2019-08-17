from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonpPat(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onpPat(self):
        expected = get_data(
            path='operations/onpPat2TE7uCuVsPpyjt2pcxdJFpB4pSVk6hA8Nvq318uuE8wdW/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onpPat2TE7uCuVsPpyjt2pcxdJFpB4pSVk6hA8Nvq318uuE8wdW/unsigned.json'))
        self.assertEqual(expected, actual)
