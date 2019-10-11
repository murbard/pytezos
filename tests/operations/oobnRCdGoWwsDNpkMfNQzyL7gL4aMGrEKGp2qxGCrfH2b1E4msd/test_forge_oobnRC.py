from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoobnRC(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oobnRC(self):
        expected = get_data(
            path='operations/oobnRCdGoWwsDNpkMfNQzyL7gL4aMGrEKGp2qxGCrfH2b1E4msd/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oobnRCdGoWwsDNpkMfNQzyL7gL4aMGrEKGp2qxGCrfH2b1E4msd/unsigned.json'))
        self.assertEqual(expected, actual)
