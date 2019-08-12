from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopQauQ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opQauQ(self):
        expected = get_data(
            path='operations/opQauQZKAfeojT2HcgihEthd1BGwPBq8BBNwLuxhnShoCyxBcRz/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opQauQZKAfeojT2HcgihEthd1BGwPBq8BBNwLuxhnShoCyxBcRz/unsigned.json'))
        self.assertEqual(expected, actual)
