from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonfX6y(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onfX6y(self):
        expected = get_data(
            path='operations/onfX6ysH8gTQSTxT5MTdAuXLWp8vVEqzXdhhzcGR1jyXdQwoZm2/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onfX6ysH8gTQSTxT5MTdAuXLWp8vVEqzXdhhzcGR1jyXdQwoZm2/unsigned.json'))
        self.assertEqual(expected, actual)
