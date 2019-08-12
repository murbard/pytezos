from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonw2Dt(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onw2Dt(self):
        expected = get_data(
            path='operations/onw2Dtyec7yR237j7P8jo9SwdMDonrb1Pa7VajiHgus3Xwoc63t/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onw2Dtyec7yR237j7P8jo9SwdMDonrb1Pa7VajiHgus3Xwoc63t/unsigned.json'))
        self.assertEqual(expected, actual)
