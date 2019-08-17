from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopSNwU(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opSNwU(self):
        expected = get_data(
            path='operations/opSNwUba4Kau5XhS3AMzmeYtAGeQnhopHPSQpPkrxtpybBYkGNA/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opSNwUba4Kau5XhS3AMzmeYtAGeQnhopHPSQpPkrxtpybBYkGNA/unsigned.json'))
        self.assertEqual(expected, actual)
