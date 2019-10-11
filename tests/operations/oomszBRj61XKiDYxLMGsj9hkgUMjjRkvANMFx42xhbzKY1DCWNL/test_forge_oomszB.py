from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoomszB(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oomszB(self):
        expected = get_data(
            path='operations/oomszBRj61XKiDYxLMGsj9hkgUMjjRkvANMFx42xhbzKY1DCWNL/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oomszBRj61XKiDYxLMGsj9hkgUMjjRkvANMFx42xhbzKY1DCWNL/unsigned.json'))
        self.assertEqual(expected, actual)
