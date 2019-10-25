from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopVkBq(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opVkBq(self):
        expected = get_data(
            path='operations/opVkBq6Jm3N6dzKZSfSCm83AvW8p11qF9bZmB5Ro28Ziwd1gLAU/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opVkBq6Jm3N6dzKZSfSCm83AvW8p11qF9bZmB5Ro28Ziwd1gLAU/unsigned.json'))
        self.assertEqual(expected, actual)
