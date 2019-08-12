from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooivF4(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooivF4(self):
        expected = get_data(
            path='operations/ooivF4n98omx9rcwb52dX3f1EVmWfwmF8ZaGpqviYqjDCfSRtGv/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooivF4n98omx9rcwb52dX3f1EVmWfwmF8ZaGpqviYqjDCfSRtGv/unsigned.json'))
        self.assertEqual(expected, actual)
