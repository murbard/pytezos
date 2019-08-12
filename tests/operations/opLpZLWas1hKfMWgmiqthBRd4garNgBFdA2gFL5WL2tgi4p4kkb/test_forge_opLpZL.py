from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopLpZL(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opLpZL(self):
        expected = get_data(
            path='operations/opLpZLWas1hKfMWgmiqthBRd4garNgBFdA2gFL5WL2tgi4p4kkb/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opLpZLWas1hKfMWgmiqthBRd4garNgBFdA2gFL5WL2tgi4p4kkb/unsigned.json'))
        self.assertEqual(expected, actual)
