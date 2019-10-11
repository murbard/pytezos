from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo2tCW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo2tCW(self):
        expected = get_data(
            path='operations/oo2tCW7XfyXcaTYeQGBhWdyDSyxQGJvcbTAn1BpsqVxUi5fXHqF/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo2tCW7XfyXcaTYeQGBhWdyDSyxQGJvcbTAn1BpsqVxUi5fXHqF/unsigned.json'))
        self.assertEqual(expected, actual)
