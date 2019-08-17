from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonuv4R(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onuv4R(self):
        expected = get_data(
            path='operations/onuv4RjixXAXjgCeEYsmF6HMazd4r3cTpHnJWqRsBj3g8N2WUHy/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onuv4RjixXAXjgCeEYsmF6HMazd4r3cTpHnJWqRsBj3g8N2WUHy/unsigned.json'))
        self.assertEqual(expected, actual)
