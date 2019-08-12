from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooyxoj(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooyxoj(self):
        expected = get_data(
            path='operations/ooyxojWy2EvBHqHJfN7gshDXmUpjgDgCoLxahb2mUW83yZCidx5/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooyxojWy2EvBHqHJfN7gshDXmUpjgDgCoLxahb2mUW83yZCidx5/unsigned.json'))
        self.assertEqual(expected, actual)
