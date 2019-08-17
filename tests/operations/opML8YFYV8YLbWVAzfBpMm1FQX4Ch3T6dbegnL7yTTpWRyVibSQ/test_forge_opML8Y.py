from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopML8Y(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opML8Y(self):
        expected = get_data(
            path='operations/opML8YFYV8YLbWVAzfBpMm1FQX4Ch3T6dbegnL7yTTpWRyVibSQ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opML8YFYV8YLbWVAzfBpMm1FQX4Ch3T6dbegnL7yTTpWRyVibSQ/unsigned.json'))
        self.assertEqual(expected, actual)
