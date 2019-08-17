from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoozaLr(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oozaLr(self):
        expected = get_data(
            path='operations/oozaLrbBarjW37Gp5apA7RZs36G14b6zXhgfJ5CXYok6pYJp2d6/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oozaLrbBarjW37Gp5apA7RZs36G14b6zXhgfJ5CXYok6pYJp2d6/unsigned.json'))
        self.assertEqual(expected, actual)
