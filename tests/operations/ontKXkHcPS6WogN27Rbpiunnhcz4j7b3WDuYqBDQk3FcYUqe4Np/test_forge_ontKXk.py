from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestontKXk(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ontKXk(self):
        expected = get_data(
            path='operations/ontKXkHcPS6WogN27Rbpiunnhcz4j7b3WDuYqBDQk3FcYUqe4Np/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ontKXkHcPS6WogN27Rbpiunnhcz4j7b3WDuYqBDQk3FcYUqe4Np/unsigned.json'))
        self.assertEqual(expected, actual)
