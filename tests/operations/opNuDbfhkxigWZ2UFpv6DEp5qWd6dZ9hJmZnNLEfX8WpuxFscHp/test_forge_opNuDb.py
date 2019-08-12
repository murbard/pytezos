from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopNuDb(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opNuDb(self):
        expected = get_data(
            path='operations/opNuDbfhkxigWZ2UFpv6DEp5qWd6dZ9hJmZnNLEfX8WpuxFscHp/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opNuDbfhkxigWZ2UFpv6DEp5qWd6dZ9hJmZnNLEfX8WpuxFscHp/unsigned.json'))
        self.assertEqual(expected, actual)
