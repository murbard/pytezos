from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopU57S(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opU57S(self):
        expected = get_data(
            path='operations/opU57SvXJdMetH7CzzCrhSDGqSciodX26u4TqG25GMYbT5UEneR/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opU57SvXJdMetH7CzzCrhSDGqSciodX26u4TqG25GMYbT5UEneR/unsigned.json'))
        self.assertEqual(expected, actual)
