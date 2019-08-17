from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonjepx(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onjepx(self):
        expected = get_data(
            path='operations/onjepx4iqV2Emd6yU3DoLtCEM8UEamQbnuJYm6meLrurCHhHEcC/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onjepx4iqV2Emd6yU3DoLtCEM8UEamQbnuJYm6meLrurCHhHEcC/unsigned.json'))
        self.assertEqual(expected, actual)
