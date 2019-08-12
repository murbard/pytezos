from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonrTu8(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onrTu8(self):
        expected = get_data(
            path='operations/onrTu8JDKTMoEJxxCne3gW1i4HrjVZKYDk96MnANQpQn2SKzjXD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onrTu8JDKTMoEJxxCne3gW1i4HrjVZKYDk96MnANQpQn2SKzjXD/unsigned.json'))
        self.assertEqual(expected, actual)
