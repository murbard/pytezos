from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooDZ1x(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooDZ1x(self):
        expected = get_data(
            path='operations/ooDZ1xhJjbWSbb835Fu2iJNv75icTM8sYXewTaNg7t6uasfveCt/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooDZ1xhJjbWSbb835Fu2iJNv75icTM8sYXewTaNg7t6uasfveCt/unsigned.json'))
        self.assertEqual(expected, actual)
