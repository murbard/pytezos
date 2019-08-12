from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopGoUu(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opGoUu(self):
        expected = get_data(
            path='operations/opGoUuL4A5Da2HqxFrpvNK29KzRSN2WLrYvDauDDBR8Y2RS5yFa/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opGoUuL4A5Da2HqxFrpvNK29KzRSN2WLrYvDauDDBR8Y2RS5yFa/unsigned.json'))
        self.assertEqual(expected, actual)
