from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopSieg(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opSieg(self):
        expected = get_data(
            path='operations/opSiegvqcZeKKXAX6eCFFGTPwxw3Co7JGBSUkqHRPnJ9T5vgvEn/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opSiegvqcZeKKXAX6eCFFGTPwxw3Co7JGBSUkqHRPnJ9T5vgvEn/unsigned.json'))
        self.assertEqual(expected, actual)
