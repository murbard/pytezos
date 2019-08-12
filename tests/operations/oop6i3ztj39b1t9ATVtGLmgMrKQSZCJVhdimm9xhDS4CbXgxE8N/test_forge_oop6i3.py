from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoop6i3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oop6i3(self):
        expected = get_data(
            path='operations/oop6i3ztj39b1t9ATVtGLmgMrKQSZCJVhdimm9xhDS4CbXgxE8N/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oop6i3ztj39b1t9ATVtGLmgMrKQSZCJVhdimm9xhDS4CbXgxE8N/unsigned.json'))
        self.assertEqual(expected, actual)
