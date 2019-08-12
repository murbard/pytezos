from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooPS4R(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooPS4R(self):
        expected = get_data(
            path='operations/ooPS4Re9BA2ExCgb5w7r36U6mbXWqkmS6TntxfveUBvd7WLiozY/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooPS4Re9BA2ExCgb5w7r36U6mbXWqkmS6TntxfveUBvd7WLiozY/unsigned.json'))
        self.assertEqual(expected, actual)
