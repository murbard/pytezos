from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooK6kP(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooK6kP(self):
        expected = get_data(
            path='operations/ooK6kPySpiEWs6U1odx8eKmKYMhmG3Smiheh8wJJRptXMGHbKkM/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooK6kPySpiEWs6U1odx8eKmKYMhmG3Smiheh8wJJRptXMGHbKkM/unsigned.json'))
        self.assertEqual(expected, actual)
