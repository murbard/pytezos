from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestongiEz(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ongiEz(self):
        expected = get_data(
            path='operations/ongiEzHw5MArY3h2dUwUHNVjgLhiNdotZhYjsxL5qiohRAMHFci/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ongiEzHw5MArY3h2dUwUHNVjgLhiNdotZhYjsxL5qiohRAMHFci/unsigned.json'))
        self.assertEqual(expected, actual)
