from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoomNw6(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oomNw6(self):
        expected = get_data(
            path='operations/oomNw63JBFnzYjDD3vCpfaYz6ctwK2kaV5WmXajC69mMa2kQXtQ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oomNw63JBFnzYjDD3vCpfaYz6ctwK2kaV5WmXajC69mMa2kQXtQ/unsigned.json'))
        self.assertEqual(expected, actual)
