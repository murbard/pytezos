from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo217M(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo217M(self):
        expected = get_data(
            path='operations/oo217M8PjuCGbBoEqCVYThio4CJ1MLEXSmeCMMygjhXy38jcMNP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo217M8PjuCGbBoEqCVYThio4CJ1MLEXSmeCMMygjhXy38jcMNP/unsigned.json'))
        self.assertEqual(expected, actual)
