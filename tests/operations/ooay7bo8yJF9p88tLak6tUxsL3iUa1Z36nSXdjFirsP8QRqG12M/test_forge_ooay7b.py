from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooay7b(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooay7b(self):
        expected = get_data(
            path='operations/ooay7bo8yJF9p88tLak6tUxsL3iUa1Z36nSXdjFirsP8QRqG12M/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooay7bo8yJF9p88tLak6tUxsL3iUa1Z36nSXdjFirsP8QRqG12M/unsigned.json'))
        self.assertEqual(expected, actual)
