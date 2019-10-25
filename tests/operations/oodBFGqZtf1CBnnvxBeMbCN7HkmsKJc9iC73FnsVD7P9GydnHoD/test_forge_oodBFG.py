from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoodBFG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oodBFG(self):
        expected = get_data(
            path='operations/oodBFGqZtf1CBnnvxBeMbCN7HkmsKJc9iC73FnsVD7P9GydnHoD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oodBFGqZtf1CBnnvxBeMbCN7HkmsKJc9iC73FnsVD7P9GydnHoD/unsigned.json'))
        self.assertEqual(expected, actual)
