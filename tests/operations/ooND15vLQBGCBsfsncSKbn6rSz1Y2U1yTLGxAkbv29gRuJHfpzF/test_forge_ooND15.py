from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooND15(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooND15(self):
        expected = get_data(
            path='operations/ooND15vLQBGCBsfsncSKbn6rSz1Y2U1yTLGxAkbv29gRuJHfpzF/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooND15vLQBGCBsfsncSKbn6rSz1Y2U1yTLGxAkbv29gRuJHfpzF/unsigned.json'))
        self.assertEqual(expected, actual)
