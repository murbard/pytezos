from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopB4jv(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opB4jv(self):
        expected = get_data(
            path='operations/opB4jvGmPdnbUvrZ2RtvDt67mZY3tMARNjMyJrPU3WYPpYze2Ku/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opB4jvGmPdnbUvrZ2RtvDt67mZY3tMARNjMyJrPU3WYPpYze2Ku/unsigned.json'))
        self.assertEqual(expected, actual)
