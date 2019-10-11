from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopWPAh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opWPAh(self):
        expected = get_data(
            path='operations/opWPAh34nhe4rj6C4nV9oqkdhCA5zWd9fHL1gXQyadF1xNmcWCw/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opWPAh34nhe4rj6C4nV9oqkdhCA5zWd9fHL1gXQyadF1xNmcWCw/unsigned.json'))
        self.assertEqual(expected, actual)
