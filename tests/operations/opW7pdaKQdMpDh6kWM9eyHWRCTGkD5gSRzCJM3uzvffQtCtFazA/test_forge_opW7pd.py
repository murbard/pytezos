from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopW7pd(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opW7pd(self):
        expected = get_data(
            path='operations/opW7pdaKQdMpDh6kWM9eyHWRCTGkD5gSRzCJM3uzvffQtCtFazA/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opW7pdaKQdMpDh6kWM9eyHWRCTGkD5gSRzCJM3uzvffQtCtFazA/unsigned.json'))
        self.assertEqual(expected, actual)
