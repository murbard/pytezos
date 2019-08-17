from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopFqRh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opFqRh(self):
        expected = get_data(
            path='operations/opFqRhLgLjNbVNt6ZujUaBLywTxEp4KSWHipU5tM5Aqjzo287E3/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opFqRhLgLjNbVNt6ZujUaBLywTxEp4KSWHipU5tM5Aqjzo287E3/unsigned.json'))
        self.assertEqual(expected, actual)
