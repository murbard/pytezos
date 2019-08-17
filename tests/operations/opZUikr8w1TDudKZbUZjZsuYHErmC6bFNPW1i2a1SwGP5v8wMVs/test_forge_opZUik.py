from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopZUik(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opZUik(self):
        expected = get_data(
            path='operations/opZUikr8w1TDudKZbUZjZsuYHErmC6bFNPW1i2a1SwGP5v8wMVs/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opZUikr8w1TDudKZbUZjZsuYHErmC6bFNPW1i2a1SwGP5v8wMVs/unsigned.json'))
        self.assertEqual(expected, actual)
