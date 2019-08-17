from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooL5Q7(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooL5Q7(self):
        expected = get_data(
            path='operations/ooL5Q7C8gFsGXdg3k2HGjMBeXtsyhfS5JLhgsNnSEaqWim7mtw2/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooL5Q7C8gFsGXdg3k2HGjMBeXtsyhfS5JLhgsNnSEaqWim7mtw2/unsigned.json'))
        self.assertEqual(expected, actual)
