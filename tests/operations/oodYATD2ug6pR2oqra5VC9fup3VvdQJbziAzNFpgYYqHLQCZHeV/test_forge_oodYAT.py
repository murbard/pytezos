from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoodYAT(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oodYAT(self):
        expected = get_data(
            path='operations/oodYATD2ug6pR2oqra5VC9fup3VvdQJbziAzNFpgYYqHLQCZHeV/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oodYATD2ug6pR2oqra5VC9fup3VvdQJbziAzNFpgYYqHLQCZHeV/unsigned.json'))
        self.assertEqual(expected, actual)
