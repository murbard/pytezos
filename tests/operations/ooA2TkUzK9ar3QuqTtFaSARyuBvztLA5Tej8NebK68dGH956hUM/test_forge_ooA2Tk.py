from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooA2Tk(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooA2Tk(self):
        expected = get_data(
            path='operations/ooA2TkUzK9ar3QuqTtFaSARyuBvztLA5Tej8NebK68dGH956hUM/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooA2TkUzK9ar3QuqTtFaSARyuBvztLA5Tej8NebK68dGH956hUM/unsigned.json'))
        self.assertEqual(expected, actual)
