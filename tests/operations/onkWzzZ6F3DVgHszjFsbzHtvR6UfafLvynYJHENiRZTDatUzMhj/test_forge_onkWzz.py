from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonkWzz(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onkWzz(self):
        expected = get_data(
            path='operations/onkWzzZ6F3DVgHszjFsbzHtvR6UfafLvynYJHENiRZTDatUzMhj/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onkWzzZ6F3DVgHszjFsbzHtvR6UfafLvynYJHENiRZTDatUzMhj/unsigned.json'))
        self.assertEqual(expected, actual)
