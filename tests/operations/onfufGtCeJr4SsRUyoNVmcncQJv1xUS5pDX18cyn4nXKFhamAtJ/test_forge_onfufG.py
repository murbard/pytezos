from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonfufG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onfufG(self):
        expected = get_data(
            path='operations/onfufGtCeJr4SsRUyoNVmcncQJv1xUS5pDX18cyn4nXKFhamAtJ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onfufGtCeJr4SsRUyoNVmcncQJv1xUS5pDX18cyn4nXKFhamAtJ/unsigned.json'))
        self.assertEqual(expected, actual)
