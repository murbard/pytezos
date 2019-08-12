from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonnEES(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onnEES(self):
        expected = get_data(
            path='operations/onnEES95kydDMURonG8JkPv1uJwee9BdXY8gca6uhdLBnRYeWJN/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onnEES95kydDMURonG8JkPv1uJwee9BdXY8gca6uhdLBnRYeWJN/unsigned.json'))
        self.assertEqual(expected, actual)
