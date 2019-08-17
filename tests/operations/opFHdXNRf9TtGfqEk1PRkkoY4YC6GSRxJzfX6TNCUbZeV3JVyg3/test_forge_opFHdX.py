from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopFHdX(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opFHdX(self):
        expected = get_data(
            path='operations/opFHdXNRf9TtGfqEk1PRkkoY4YC6GSRxJzfX6TNCUbZeV3JVyg3/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opFHdXNRf9TtGfqEk1PRkkoY4YC6GSRxJzfX6TNCUbZeV3JVyg3/unsigned.json'))
        self.assertEqual(expected, actual)
