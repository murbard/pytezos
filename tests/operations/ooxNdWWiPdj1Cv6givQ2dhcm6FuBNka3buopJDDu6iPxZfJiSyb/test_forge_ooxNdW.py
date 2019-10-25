from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooxNdW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooxNdW(self):
        expected = get_data(
            path='operations/ooxNdWWiPdj1Cv6givQ2dhcm6FuBNka3buopJDDu6iPxZfJiSyb/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooxNdWWiPdj1Cv6givQ2dhcm6FuBNka3buopJDDu6iPxZfJiSyb/unsigned.json'))
        self.assertEqual(expected, actual)
