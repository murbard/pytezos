from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooMETD(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooMETD(self):
        expected = get_data(
            path='operations/ooMETDbcAENFtP9S2s6mFBXaptcmMhLJNYaa4cwbnL1yBuJoPKk/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooMETDbcAENFtP9S2s6mFBXaptcmMhLJNYaa4cwbnL1yBuJoPKk/unsigned.json'))
        self.assertEqual(expected, actual)
