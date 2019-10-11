from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooEL3U(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooEL3U(self):
        expected = get_data(
            path='operations/ooEL3UNdHwYEgtneXsCU4JuNGW4LxCDDCiDojoueRt3QHytqP6T/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooEL3UNdHwYEgtneXsCU4JuNGW4LxCDDCiDojoueRt3QHytqP6T/unsigned.json'))
        self.assertEqual(expected, actual)
