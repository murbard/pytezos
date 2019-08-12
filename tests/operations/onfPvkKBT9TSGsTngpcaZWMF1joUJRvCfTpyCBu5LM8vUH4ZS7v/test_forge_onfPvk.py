from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonfPvk(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onfPvk(self):
        expected = get_data(
            path='operations/onfPvkKBT9TSGsTngpcaZWMF1joUJRvCfTpyCBu5LM8vUH4ZS7v/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onfPvkKBT9TSGsTngpcaZWMF1joUJRvCfTpyCBu5LM8vUH4ZS7v/unsigned.json'))
        self.assertEqual(expected, actual)
