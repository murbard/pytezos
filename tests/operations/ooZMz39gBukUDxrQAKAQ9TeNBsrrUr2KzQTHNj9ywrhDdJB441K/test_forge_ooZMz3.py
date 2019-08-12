from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooZMz3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooZMz3(self):
        expected = get_data(
            path='operations/ooZMz39gBukUDxrQAKAQ9TeNBsrrUr2KzQTHNj9ywrhDdJB441K/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooZMz39gBukUDxrQAKAQ9TeNBsrrUr2KzQTHNj9ywrhDdJB441K/unsigned.json'))
        self.assertEqual(expected, actual)
