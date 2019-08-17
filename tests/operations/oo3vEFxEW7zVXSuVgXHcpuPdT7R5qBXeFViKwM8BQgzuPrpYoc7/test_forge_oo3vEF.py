from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo3vEF(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo3vEF(self):
        expected = get_data(
            path='operations/oo3vEFxEW7zVXSuVgXHcpuPdT7R5qBXeFViKwM8BQgzuPrpYoc7/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo3vEFxEW7zVXSuVgXHcpuPdT7R5qBXeFViKwM8BQgzuPrpYoc7/unsigned.json'))
        self.assertEqual(expected, actual)
