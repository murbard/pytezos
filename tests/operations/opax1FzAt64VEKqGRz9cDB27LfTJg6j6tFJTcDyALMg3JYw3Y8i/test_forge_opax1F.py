from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopax1F(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opax1F(self):
        expected = get_data(
            path='operations/opax1FzAt64VEKqGRz9cDB27LfTJg6j6tFJTcDyALMg3JYw3Y8i/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opax1FzAt64VEKqGRz9cDB27LfTJg6j6tFJTcDyALMg3JYw3Y8i/unsigned.json'))
        self.assertEqual(expected, actual)
