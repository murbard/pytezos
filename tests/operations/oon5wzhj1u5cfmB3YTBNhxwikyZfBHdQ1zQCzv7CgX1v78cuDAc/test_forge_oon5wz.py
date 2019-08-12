from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoon5wz(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oon5wz(self):
        expected = get_data(
            path='operations/oon5wzhj1u5cfmB3YTBNhxwikyZfBHdQ1zQCzv7CgX1v78cuDAc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oon5wzhj1u5cfmB3YTBNhxwikyZfBHdQ1zQCzv7CgX1v78cuDAc/unsigned.json'))
        self.assertEqual(expected, actual)
