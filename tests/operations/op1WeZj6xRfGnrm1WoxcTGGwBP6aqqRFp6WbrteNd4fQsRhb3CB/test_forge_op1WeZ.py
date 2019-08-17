from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop1WeZ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op1WeZ(self):
        expected = get_data(
            path='operations/op1WeZj6xRfGnrm1WoxcTGGwBP6aqqRFp6WbrteNd4fQsRhb3CB/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op1WeZj6xRfGnrm1WoxcTGGwBP6aqqRFp6WbrteNd4fQsRhb3CB/unsigned.json'))
        self.assertEqual(expected, actual)
