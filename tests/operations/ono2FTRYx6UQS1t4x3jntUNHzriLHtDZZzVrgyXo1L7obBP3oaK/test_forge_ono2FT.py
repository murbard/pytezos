from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestono2FT(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ono2FT(self):
        expected = get_data(
            path='operations/ono2FTRYx6UQS1t4x3jntUNHzriLHtDZZzVrgyXo1L7obBP3oaK/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ono2FTRYx6UQS1t4x3jntUNHzriLHtDZZzVrgyXo1L7obBP3oaK/unsigned.json'))
        self.assertEqual(expected, actual)
