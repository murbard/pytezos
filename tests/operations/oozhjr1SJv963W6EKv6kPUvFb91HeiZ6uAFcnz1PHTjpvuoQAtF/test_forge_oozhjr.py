from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoozhjr(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oozhjr(self):
        expected = get_data(
            path='operations/oozhjr1SJv963W6EKv6kPUvFb91HeiZ6uAFcnz1PHTjpvuoQAtF/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oozhjr1SJv963W6EKv6kPUvFb91HeiZ6uAFcnz1PHTjpvuoQAtF/unsigned.json'))
        self.assertEqual(expected, actual)
