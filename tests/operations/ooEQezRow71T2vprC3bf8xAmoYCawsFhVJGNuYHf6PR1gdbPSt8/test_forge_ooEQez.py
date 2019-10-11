from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooEQez(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooEQez(self):
        expected = get_data(
            path='operations/ooEQezRow71T2vprC3bf8xAmoYCawsFhVJGNuYHf6PR1gdbPSt8/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooEQezRow71T2vprC3bf8xAmoYCawsFhVJGNuYHf6PR1gdbPSt8/unsigned.json'))
        self.assertEqual(expected, actual)
