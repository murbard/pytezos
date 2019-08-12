from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooBVXs(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooBVXs(self):
        expected = get_data(
            path='operations/ooBVXs25WLUZcEFSvQyeij82cRP2Bq6Urw5zKASx5VAmudbtg7o/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooBVXs25WLUZcEFSvQyeij82cRP2Bq6Urw5zKASx5VAmudbtg7o/unsigned.json'))
        self.assertEqual(expected, actual)
