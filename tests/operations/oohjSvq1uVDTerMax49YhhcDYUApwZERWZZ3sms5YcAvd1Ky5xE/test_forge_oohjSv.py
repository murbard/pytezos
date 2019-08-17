from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoohjSv(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oohjSv(self):
        expected = get_data(
            path='operations/oohjSvq1uVDTerMax49YhhcDYUApwZERWZZ3sms5YcAvd1Ky5xE/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oohjSvq1uVDTerMax49YhhcDYUApwZERWZZ3sms5YcAvd1Ky5xE/unsigned.json'))
        self.assertEqual(expected, actual)
