from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonkzjB(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onkzjB(self):
        expected = get_data(
            path='operations/onkzjBnbWD3xiZ57wFAenMsCqYZ234aS5faMFMK7WygpZVYgBs7/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onkzjBnbWD3xiZ57wFAenMsCqYZ234aS5faMFMK7WygpZVYgBs7/unsigned.json'))
        self.assertEqual(expected, actual)
