from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo6ohN(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo6ohN(self):
        expected = get_data(
            path='operations/oo6ohNj5BwHrsrYeVF99unmEYajPbHURKw8HVAxapFwbr5umrK5/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo6ohNj5BwHrsrYeVF99unmEYajPbHURKw8HVAxapFwbr5umrK5/unsigned.json'))
        self.assertEqual(expected, actual)
