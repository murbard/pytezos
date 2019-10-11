from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoonJQx(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oonJQx(self):
        expected = get_data(
            path='operations/oonJQx2n9Ty2f9xfFHqKrodeziFgKHdcdfHqTw9pU1GgruXPwBS/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oonJQx2n9Ty2f9xfFHqKrodeziFgKHdcdfHqTw9pU1GgruXPwBS/unsigned.json'))
        self.assertEqual(expected, actual)
