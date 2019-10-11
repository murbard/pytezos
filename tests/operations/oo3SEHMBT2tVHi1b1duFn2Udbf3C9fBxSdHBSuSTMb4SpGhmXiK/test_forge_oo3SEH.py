from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo3SEH(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo3SEH(self):
        expected = get_data(
            path='operations/oo3SEHMBT2tVHi1b1duFn2Udbf3C9fBxSdHBSuSTMb4SpGhmXiK/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo3SEHMBT2tVHi1b1duFn2Udbf3C9fBxSdHBSuSTMb4SpGhmXiK/unsigned.json'))
        self.assertEqual(expected, actual)
