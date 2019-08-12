from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooEFna(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooEFna(self):
        expected = get_data(
            path='operations/ooEFna2TyTctrzUCThrtxe3hKHtjfHkShM2qCfu24yQ5PBB47Y4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooEFna2TyTctrzUCThrtxe3hKHtjfHkShM2qCfu24yQ5PBB47Y4/unsigned.json'))
        self.assertEqual(expected, actual)
