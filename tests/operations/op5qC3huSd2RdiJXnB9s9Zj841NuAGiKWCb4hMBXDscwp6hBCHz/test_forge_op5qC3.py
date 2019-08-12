from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop5qC3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op5qC3(self):
        expected = get_data(
            path='operations/op5qC3huSd2RdiJXnB9s9Zj841NuAGiKWCb4hMBXDscwp6hBCHz/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op5qC3huSd2RdiJXnB9s9Zj841NuAGiKWCb4hMBXDscwp6hBCHz/unsigned.json'))
        self.assertEqual(expected, actual)
