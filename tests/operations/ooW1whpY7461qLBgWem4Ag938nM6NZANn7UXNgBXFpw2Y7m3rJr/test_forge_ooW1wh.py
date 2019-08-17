from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooW1wh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooW1wh(self):
        expected = get_data(
            path='operations/ooW1whpY7461qLBgWem4Ag938nM6NZANn7UXNgBXFpw2Y7m3rJr/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooW1whpY7461qLBgWem4Ag938nM6NZANn7UXNgBXFpw2Y7m3rJr/unsigned.json'))
        self.assertEqual(expected, actual)
