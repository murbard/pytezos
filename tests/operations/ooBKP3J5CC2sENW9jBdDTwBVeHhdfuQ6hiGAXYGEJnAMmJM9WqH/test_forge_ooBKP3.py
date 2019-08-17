from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooBKP3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooBKP3(self):
        expected = get_data(
            path='operations/ooBKP3J5CC2sENW9jBdDTwBVeHhdfuQ6hiGAXYGEJnAMmJM9WqH/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooBKP3J5CC2sENW9jBdDTwBVeHhdfuQ6hiGAXYGEJnAMmJM9WqH/unsigned.json'))
        self.assertEqual(expected, actual)
