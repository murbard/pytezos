from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoooJR5(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oooJR5(self):
        expected = get_data(
            path='operations/oooJR5BpuKcTpKUm9QgdkqfK38wYNcaH4xPS1GSrvzdWsr5RSFP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oooJR5BpuKcTpKUm9QgdkqfK38wYNcaH4xPS1GSrvzdWsr5RSFP/unsigned.json'))
        self.assertEqual(expected, actual)
