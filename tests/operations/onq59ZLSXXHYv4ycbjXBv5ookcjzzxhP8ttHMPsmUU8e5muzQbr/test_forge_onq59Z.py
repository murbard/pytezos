from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonq59Z(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onq59Z(self):
        expected = get_data(
            path='operations/onq59ZLSXXHYv4ycbjXBv5ookcjzzxhP8ttHMPsmUU8e5muzQbr/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onq59ZLSXXHYv4ycbjXBv5ookcjzzxhP8ttHMPsmUU8e5muzQbr/unsigned.json'))
        self.assertEqual(expected, actual)
