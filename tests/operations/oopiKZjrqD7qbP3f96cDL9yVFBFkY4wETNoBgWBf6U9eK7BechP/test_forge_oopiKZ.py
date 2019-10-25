from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoopiKZ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oopiKZ(self):
        expected = get_data(
            path='operations/oopiKZjrqD7qbP3f96cDL9yVFBFkY4wETNoBgWBf6U9eK7BechP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oopiKZjrqD7qbP3f96cDL9yVFBFkY4wETNoBgWBf6U9eK7BechP/unsigned.json'))
        self.assertEqual(expected, actual)
