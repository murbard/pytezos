from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopYaYM(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opYaYM(self):
        expected = get_data(
            path='operations/opYaYMPaitztvbifz1MyPSa2ZjqMHeUPCEXK1a74yFGD1RyGSRj/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opYaYMPaitztvbifz1MyPSa2ZjqMHeUPCEXK1a74yFGD1RyGSRj/unsigned.json'))
        self.assertEqual(expected, actual)
