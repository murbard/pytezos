from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooZWSJ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooZWSJ(self):
        expected = get_data(
            path='operations/ooZWSJqGRqi4hirFmqvFinKp9JGU3vqR23Q15tMvDXMnWtX1jne/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooZWSJqGRqi4hirFmqvFinKp9JGU3vqR23Q15tMvDXMnWtX1jne/unsigned.json'))
        self.assertEqual(expected, actual)
