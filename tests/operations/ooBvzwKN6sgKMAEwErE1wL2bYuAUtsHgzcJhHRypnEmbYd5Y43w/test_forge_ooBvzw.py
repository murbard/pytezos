from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooBvzw(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooBvzw(self):
        expected = get_data(
            path='operations/ooBvzwKN6sgKMAEwErE1wL2bYuAUtsHgzcJhHRypnEmbYd5Y43w/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooBvzwKN6sgKMAEwErE1wL2bYuAUtsHgzcJhHRypnEmbYd5Y43w/unsigned.json'))
        self.assertEqual(expected, actual)
