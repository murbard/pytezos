from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonxXT4(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onxXT4(self):
        expected = get_data(
            path='operations/onxXT4eyxMTvQRv8cKZT12q1jcr2ZgxzdGH9EyfkpFSVNswEYqE/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onxXT4eyxMTvQRv8cKZT12q1jcr2ZgxzdGH9EyfkpFSVNswEYqE/unsigned.json'))
        self.assertEqual(expected, actual)
