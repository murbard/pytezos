from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonw4Ci(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onw4Ci(self):
        expected = get_data(
            path='operations/onw4CiDAXGLUpSJVe2UCMjkEddmbpgwtdZgtBNWNvzcwWAdSnEq/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onw4CiDAXGLUpSJVe2UCMjkEddmbpgwtdZgtBNWNvzcwWAdSnEq/unsigned.json'))
        self.assertEqual(expected, actual)
