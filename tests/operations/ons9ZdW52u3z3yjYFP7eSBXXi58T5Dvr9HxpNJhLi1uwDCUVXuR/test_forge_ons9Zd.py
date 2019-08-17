from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestons9Zd(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ons9Zd(self):
        expected = get_data(
            path='operations/ons9ZdW52u3z3yjYFP7eSBXXi58T5Dvr9HxpNJhLi1uwDCUVXuR/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ons9ZdW52u3z3yjYFP7eSBXXi58T5Dvr9HxpNJhLi1uwDCUVXuR/unsigned.json'))
        self.assertEqual(expected, actual)
