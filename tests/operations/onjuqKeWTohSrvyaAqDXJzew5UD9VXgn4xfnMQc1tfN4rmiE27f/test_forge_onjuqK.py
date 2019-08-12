from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonjuqK(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onjuqK(self):
        expected = get_data(
            path='operations/onjuqKeWTohSrvyaAqDXJzew5UD9VXgn4xfnMQc1tfN4rmiE27f/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onjuqKeWTohSrvyaAqDXJzew5UD9VXgn4xfnMQc1tfN4rmiE27f/unsigned.json'))
        self.assertEqual(expected, actual)
