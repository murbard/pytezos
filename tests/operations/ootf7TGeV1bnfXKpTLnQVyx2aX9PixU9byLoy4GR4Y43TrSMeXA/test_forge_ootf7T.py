from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestootf7T(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ootf7T(self):
        expected = get_data(
            path='operations/ootf7TGeV1bnfXKpTLnQVyx2aX9PixU9byLoy4GR4Y43TrSMeXA/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ootf7TGeV1bnfXKpTLnQVyx2aX9PixU9byLoy4GR4Y43TrSMeXA/unsigned.json'))
        self.assertEqual(expected, actual)
