from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopKHkD(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opKHkD(self):
        expected = get_data(
            path='operations/opKHkDp7h1iesF9WfWmn35tMDc3LMg8n8n4cbi45gJju75JLcvS/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opKHkDp7h1iesF9WfWmn35tMDc3LMg8n8n4cbi45gJju75JLcvS/unsigned.json'))
        self.assertEqual(expected, actual)
