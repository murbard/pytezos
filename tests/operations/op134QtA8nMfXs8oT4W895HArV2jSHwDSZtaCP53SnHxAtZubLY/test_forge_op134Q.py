from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop134Q(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op134Q(self):
        expected = get_data(
            path='operations/op134QtA8nMfXs8oT4W895HArV2jSHwDSZtaCP53SnHxAtZubLY/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op134QtA8nMfXs8oT4W895HArV2jSHwDSZtaCP53SnHxAtZubLY/unsigned.json'))
        self.assertEqual(expected, actual)
