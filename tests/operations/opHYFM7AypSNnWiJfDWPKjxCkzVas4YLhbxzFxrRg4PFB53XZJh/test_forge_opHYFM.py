from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopHYFM(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opHYFM(self):
        expected = get_data(
            path='operations/opHYFM7AypSNnWiJfDWPKjxCkzVas4YLhbxzFxrRg4PFB53XZJh/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opHYFM7AypSNnWiJfDWPKjxCkzVas4YLhbxzFxrRg4PFB53XZJh/unsigned.json'))
        self.assertEqual(expected, actual)
