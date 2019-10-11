from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonuDGh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onuDGh(self):
        expected = get_data(
            path='operations/onuDGhuS1D9hcPjf8uivyMLco1ZqBpVBQj4Dnz6vzybrQgDXpfc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onuDGhuS1D9hcPjf8uivyMLco1ZqBpVBQj4Dnz6vzybrQgDXpfc/unsigned.json'))
        self.assertEqual(expected, actual)
