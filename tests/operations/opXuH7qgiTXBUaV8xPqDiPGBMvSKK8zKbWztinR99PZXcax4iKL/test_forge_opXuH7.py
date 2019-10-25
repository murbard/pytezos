from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopXuH7(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opXuH7(self):
        expected = get_data(
            path='operations/opXuH7qgiTXBUaV8xPqDiPGBMvSKK8zKbWztinR99PZXcax4iKL/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opXuH7qgiTXBUaV8xPqDiPGBMvSKK8zKbWztinR99PZXcax4iKL/unsigned.json'))
        self.assertEqual(expected, actual)
