from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestongxpT(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ongxpT(self):
        expected = get_data(
            path='operations/ongxpTr4mjR5PnFKD3yWvFCnyQpT1zB9KuE89AzX1ezkAhQsVJw/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ongxpTr4mjR5PnFKD3yWvFCnyQpT1zB9KuE89AzX1ezkAhQsVJw/unsigned.json'))
        self.assertEqual(expected, actual)
