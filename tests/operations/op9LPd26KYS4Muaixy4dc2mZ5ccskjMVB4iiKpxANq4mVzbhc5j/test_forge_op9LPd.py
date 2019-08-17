from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop9LPd(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op9LPd(self):
        expected = get_data(
            path='operations/op9LPd26KYS4Muaixy4dc2mZ5ccskjMVB4iiKpxANq4mVzbhc5j/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op9LPd26KYS4Muaixy4dc2mZ5ccskjMVB4iiKpxANq4mVzbhc5j/unsigned.json'))
        self.assertEqual(expected, actual)
