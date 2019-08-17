from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestontMDk(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ontMDk(self):
        expected = get_data(
            path='operations/ontMDkNMyGhrYd9QB2GftqkpiLiadWkewW5xQDTZ1tgUJ3haRqc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ontMDkNMyGhrYd9QB2GftqkpiLiadWkewW5xQDTZ1tgUJ3haRqc/unsigned.json'))
        self.assertEqual(expected, actual)
