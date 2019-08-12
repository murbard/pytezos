from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop5x9X(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op5x9X(self):
        expected = get_data(
            path='operations/op5x9Xj9xRvCr4RiUodAt8AFx8a7iSqiHn4naAN1UpqPHCVw5Ek/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op5x9Xj9xRvCr4RiUodAt8AFx8a7iSqiHn4naAN1UpqPHCVw5Ek/unsigned.json'))
        self.assertEqual(expected, actual)
