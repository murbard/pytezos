from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooU3P3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooU3P3(self):
        expected = get_data(
            path='operations/ooU3P36nEKanCgUN1ZdVcABxwKbuRzrwjDASzUaD2jMbk4nqvu5/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooU3P36nEKanCgUN1ZdVcABxwKbuRzrwjDASzUaD2jMbk4nqvu5/unsigned.json'))
        self.assertEqual(expected, actual)
