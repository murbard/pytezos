from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoonBHS(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oonBHS(self):
        expected = get_data(
            path='operations/oonBHSvthfjezqqJEzg7W7uERGeWoFU8uZF9T5935X2ZjBmQx5T/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oonBHSvthfjezqqJEzg7W7uERGeWoFU8uZF9T5935X2ZjBmQx5T/unsigned.json'))
        self.assertEqual(expected, actual)
