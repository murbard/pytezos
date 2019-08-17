from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooh48o(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooh48o(self):
        expected = get_data(
            path='operations/ooh48oxiTS6ueV7cBpbpLueftgJwyrtrw7tMRhdZA31NiJHar6x/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooh48oxiTS6ueV7cBpbpLueftgJwyrtrw7tMRhdZA31NiJHar6x/unsigned.json'))
        self.assertEqual(expected, actual)
