from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop7mAF(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op7mAF(self):
        expected = get_data(
            path='operations/op7mAFz3JbjDqRPVngceBb9Ek3D6MiXPB9x7amSpz9Qe9aLeiiX/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op7mAFz3JbjDqRPVngceBb9Ek3D6MiXPB9x7amSpz9Qe9aLeiiX/unsigned.json'))
        self.assertEqual(expected, actual)
