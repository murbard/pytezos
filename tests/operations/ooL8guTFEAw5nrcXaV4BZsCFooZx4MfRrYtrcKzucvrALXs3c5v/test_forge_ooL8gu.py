from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooL8gu(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooL8gu(self):
        expected = get_data(
            path='operations/ooL8guTFEAw5nrcXaV4BZsCFooZx4MfRrYtrcKzucvrALXs3c5v/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooL8guTFEAw5nrcXaV4BZsCFooZx4MfRrYtrcKzucvrALXs3c5v/unsigned.json'))
        self.assertEqual(expected, actual)
