from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooyvRt(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooyvRt(self):
        expected = get_data(
            path='operations/ooyvRt78AVNz815WdfFALSrusiac9pS3jbj2G4joBAqs7W8tWg3/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooyvRt78AVNz815WdfFALSrusiac9pS3jbj2G4joBAqs7W8tWg3/unsigned.json'))
        self.assertEqual(expected, actual)
