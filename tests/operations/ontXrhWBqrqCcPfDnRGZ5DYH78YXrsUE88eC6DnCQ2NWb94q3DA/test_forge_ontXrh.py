from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestontXrh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ontXrh(self):
        expected = get_data(
            path='operations/ontXrhWBqrqCcPfDnRGZ5DYH78YXrsUE88eC6DnCQ2NWb94q3DA/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ontXrhWBqrqCcPfDnRGZ5DYH78YXrsUE88eC6DnCQ2NWb94q3DA/unsigned.json'))
        self.assertEqual(expected, actual)
