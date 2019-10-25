from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooFDEN(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooFDEN(self):
        expected = get_data(
            path='operations/ooFDENTDXmm2TMUugi3B8J93tprk3qRJajD9Djw2ESamNuCbZod/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooFDENTDXmm2TMUugi3B8J93tprk3qRJajD9Djw2ESamNuCbZod/unsigned.json'))
        self.assertEqual(expected, actual)
