from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopDx5o(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opDx5o(self):
        expected = get_data(
            path='operations/opDx5o84SQGPeUffMiPGckBMoN6K9qpUPowJfkQwPbFN2f1Ymjf/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opDx5o84SQGPeUffMiPGckBMoN6K9qpUPowJfkQwPbFN2f1Ymjf/unsigned.json'))
        self.assertEqual(expected, actual)
