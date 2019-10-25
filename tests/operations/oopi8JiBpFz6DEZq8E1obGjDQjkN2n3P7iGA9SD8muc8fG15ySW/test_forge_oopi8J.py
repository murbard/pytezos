from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoopi8J(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oopi8J(self):
        expected = get_data(
            path='operations/oopi8JiBpFz6DEZq8E1obGjDQjkN2n3P7iGA9SD8muc8fG15ySW/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oopi8JiBpFz6DEZq8E1obGjDQjkN2n3P7iGA9SD8muc8fG15ySW/unsigned.json'))
        self.assertEqual(expected, actual)
