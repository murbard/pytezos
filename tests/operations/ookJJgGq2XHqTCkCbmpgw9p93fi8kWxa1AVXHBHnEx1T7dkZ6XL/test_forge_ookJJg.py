from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestookJJg(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ookJJg(self):
        expected = get_data(
            path='operations/ookJJgGq2XHqTCkCbmpgw9p93fi8kWxa1AVXHBHnEx1T7dkZ6XL/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ookJJgGq2XHqTCkCbmpgw9p93fi8kWxa1AVXHBHnEx1T7dkZ6XL/unsigned.json'))
        self.assertEqual(expected, actual)
