from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo9tJW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo9tJW(self):
        expected = get_data(
            path='operations/oo9tJWAeBXJWNh62Gi2MBNduCHuXV8LiuFdFcYLuadaS3y4jLRf/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo9tJWAeBXJWNh62Gi2MBNduCHuXV8LiuFdFcYLuadaS3y4jLRf/unsigned.json'))
        self.assertEqual(expected, actual)
