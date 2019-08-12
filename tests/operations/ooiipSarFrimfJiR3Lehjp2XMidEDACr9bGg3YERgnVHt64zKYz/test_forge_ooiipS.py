from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooiipS(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooiipS(self):
        expected = get_data(
            path='operations/ooiipSarFrimfJiR3Lehjp2XMidEDACr9bGg3YERgnVHt64zKYz/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooiipSarFrimfJiR3Lehjp2XMidEDACr9bGg3YERgnVHt64zKYz/unsigned.json'))
        self.assertEqual(expected, actual)
