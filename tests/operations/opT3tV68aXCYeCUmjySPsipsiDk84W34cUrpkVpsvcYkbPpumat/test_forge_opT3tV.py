from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopT3tV(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opT3tV(self):
        expected = get_data(
            path='operations/opT3tV68aXCYeCUmjySPsipsiDk84W34cUrpkVpsvcYkbPpumat/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opT3tV68aXCYeCUmjySPsipsiDk84W34cUrpkVpsvcYkbPpumat/unsigned.json'))
        self.assertEqual(expected, actual)
