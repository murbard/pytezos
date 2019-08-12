from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoneQCm(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oneQCm(self):
        expected = get_data(
            path='operations/oneQCm7ePUg7kE3D9Rit7bpJFrfBKgVVPJHdkuQJGPXSYh7XB2V/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oneQCm7ePUg7kE3D9Rit7bpJFrfBKgVVPJHdkuQJGPXSYh7XB2V/unsigned.json'))
        self.assertEqual(expected, actual)
