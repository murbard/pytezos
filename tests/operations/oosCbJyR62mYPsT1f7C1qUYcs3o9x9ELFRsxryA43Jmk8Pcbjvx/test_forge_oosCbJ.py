from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoosCbJ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oosCbJ(self):
        expected = get_data(
            path='operations/oosCbJyR62mYPsT1f7C1qUYcs3o9x9ELFRsxryA43Jmk8Pcbjvx/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oosCbJyR62mYPsT1f7C1qUYcs3o9x9ELFRsxryA43Jmk8Pcbjvx/unsigned.json'))
        self.assertEqual(expected, actual)
