from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooR1CF(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooR1CF(self):
        expected = get_data(
            path='operations/ooR1CFPnC33f6bu6mnQdwN6aybffYaBfptmjFQMYy3JfM8NGd9M/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooR1CFPnC33f6bu6mnQdwN6aybffYaBfptmjFQMYy3JfM8NGd9M/unsigned.json'))
        self.assertEqual(expected, actual)
