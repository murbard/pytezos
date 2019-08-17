from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopMPxi(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opMPxi(self):
        expected = get_data(
            path='operations/opMPxiTmvSTFyYQPgnPZGvxjgfYUPcagTg3PPiTRLxYzYBYH3WR/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opMPxiTmvSTFyYQPgnPZGvxjgfYUPcagTg3PPiTRLxYzYBYH3WR/unsigned.json'))
        self.assertEqual(expected, actual)
