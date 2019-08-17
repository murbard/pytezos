from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonjhoN(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onjhoN(self):
        expected = get_data(
            path='operations/onjhoNQsLdLZbSB5W87eu683jkhEmCqvUkys8VtDnDuZCEBBPEv/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onjhoNQsLdLZbSB5W87eu683jkhEmCqvUkys8VtDnDuZCEBBPEv/unsigned.json'))
        self.assertEqual(expected, actual)
