from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopJu3P(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opJu3P(self):
        expected = get_data(
            path='operations/opJu3P9JfL4HAs5biRsLgRYS8eWndMXez5DyCopFkuGt5wm6q3Q/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opJu3P9JfL4HAs5biRsLgRYS8eWndMXez5DyCopFkuGt5wm6q3Q/unsigned.json'))
        self.assertEqual(expected, actual)
