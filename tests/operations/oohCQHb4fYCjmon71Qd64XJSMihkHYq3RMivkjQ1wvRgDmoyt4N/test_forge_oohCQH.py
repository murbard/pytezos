from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoohCQH(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oohCQH(self):
        expected = get_data(
            path='operations/oohCQHb4fYCjmon71Qd64XJSMihkHYq3RMivkjQ1wvRgDmoyt4N/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oohCQHb4fYCjmon71Qd64XJSMihkHYq3RMivkjQ1wvRgDmoyt4N/unsigned.json'))
        self.assertEqual(expected, actual)
