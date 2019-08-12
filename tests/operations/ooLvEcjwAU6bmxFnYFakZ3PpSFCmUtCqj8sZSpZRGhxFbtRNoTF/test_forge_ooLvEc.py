from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooLvEc(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooLvEc(self):
        expected = get_data(
            path='operations/ooLvEcjwAU6bmxFnYFakZ3PpSFCmUtCqj8sZSpZRGhxFbtRNoTF/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooLvEcjwAU6bmxFnYFakZ3PpSFCmUtCqj8sZSpZRGhxFbtRNoTF/unsigned.json'))
        self.assertEqual(expected, actual)
