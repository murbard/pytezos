from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopTwZx(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opTwZx(self):
        expected = get_data(
            path='operations/opTwZxAR5CtYHoHzbZuDr2C3jkEzHfSEFo1MHTPn7yaunDDLJJN/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opTwZxAR5CtYHoHzbZuDr2C3jkEzHfSEFo1MHTPn7yaunDDLJJN/unsigned.json'))
        self.assertEqual(expected, actual)
