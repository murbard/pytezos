from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop5tRG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op5tRG(self):
        expected = get_data(
            path='operations/op5tRGLz48GiquuMJQuyLqKk46VCXiY8ZLueAjVjGtvdKveiDJW/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op5tRGLz48GiquuMJQuyLqKk46VCXiY8ZLueAjVjGtvdKveiDJW/unsigned.json'))
        self.assertEqual(expected, actual)
