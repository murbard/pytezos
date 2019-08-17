from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestongvxA(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ongvxA(self):
        expected = get_data(
            path='operations/ongvxAASw11TXV64dUCCA81Yg4MHxii3c2kcekNAA6Gd4n69rGj/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ongvxAASw11TXV64dUCCA81Yg4MHxii3c2kcekNAA6Gd4n69rGj/unsigned.json'))
        self.assertEqual(expected, actual)
